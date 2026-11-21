import requests

r = requests.get(
    "https://nominatim.openstreetmap.org/search",
    params={"q": "Nørrebrogade København", "format": "json", "limit": 1},
    headers={"User-Agent": "aslak-learning/0.1"},
)
print(r.status_code)
print(r.url)
data = r.json()
print(data[0]["lat"], data[0]["lon"])

lat = float(data[0]["lat"])   # Nominatim returns strings -> convert to numbers
lon = float(data[0]["lon"])

query = f"""
[out:json][timeout:25];
nwr["amenity"="cafe"]["name"](around:500,{lat},{lon});
out center 5;
"""

r2 = requests.post(
    "https://overpass-api.de/api/interpreter",
    data={"data": query},
    headers={"User-Agent": "aslak-learning/0.1"},
)

if r2.status_code != 200:
    print("Overpass error:", r2.status_code)
    print(r2.text[:300])      # show what the server actually sent
    raise SystemExit
result = r2.json()

print(r2.status_code)          # 200 = ok, 429 = too many requests, 504 = server busy
result = r2.json()
print(result.keys())           # see the top-level structure

for el in result["elements"]:
    if el["type"] == "node":
        point = el                 # a point on the map: lat/lon directly
    else:
        point = el["center"]       # a building (way/relation): only a center
    print(el["type"], el["tags"]["name"], point["lat"], point["lon"])