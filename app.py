import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv
import requests
import time

load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)

FEEDBACK_FILE = os.path.join(DATA_DIR, "feedback.jsonl")
STATE_FILE = os.path.join(DATA_DIR, "app_state.json")

user_agent = "trip-planner-capstone/1.0 (aslak.bennedsen@gmail.com)"
headers = {"User-Agent": user_agent}

NOVATIM_URL = "https://nominatim.openstreetmap.org/search"
OVERPASS_URL = "https://overpass-api.de/api/interpreter"


@st.cache_data
def geocoder(city):
    for attempt in range(4):
        try:
            r = requests.get(
                NOVATIM_URL,
                params={"q": city, "format": "json", "limit": 1},
                headers=headers,
                timeout=15
            )
            if r.status_code == 200:
                results = r.json()
                if not results:
                    return None                       # nothing found
                top = results[0]
            
                return float(top["lat"]), float(top["lon"]), top["display_name"]
        except requests.RequestException:
            pass
        time.sleep(2 ** attempt)
    return None

CATEGORIES = {
    "Restaurants": ("amenity", "restaurant"),
    "Cafés":       ("amenity", "cafe"),
    "Museums":     ("tourism", "museum"),
    "Parks":       ("leisure", "park"),
    "Attractions": ("tourism", "attraction"),
}

@st.cache_data
def find_pois(lat, lon, category, radius=1000, limit=20):
    key, value = CATEGORIES[category]
    query = f"""
    [out:json][timeout:30];
    nwr["{key}"="{value}"]["name"](around:{radius},{lat},{lon});
    out center {limit};
    """
    for attempt in range(4):
        try:
            r = requests.post(
                OVERPASS_URL,
                data={"data": query},
                headers=headers,
                timeout=25
            )
            if r.status_code == 200:
                results = r.json()
                elements = results.get("elements", [])
                list_of_elements = []

                for element in elements:
                    tags = element.get("tags", {})
                    list_of_elements.append({"poi_id":f"{element['type']}/{element['id']}", "name": tags.get("name"), 
                                             "category": category, "lat": element.get("lat") or element.get("center", {}).get("lat"), "lon": element.get("lon") or element.get("center", {}).get("lon"), 
                                             "url": tags.get("website") or "No website found"})
                return list_of_elements
            print("Overpass status:", r.status_code, r.text[:300]) 
        except requests.RequestException as e:
            print("Overpass error:", e)  
        time.sleep(2 ** attempt)
    return None

@st.cache_data
def rag_wikivoyage(destination):
    


    # POST it with headers=HEADERS and timeout=30, check status_code,
    # then loop over "elements" and return a list of dicts with name, lat, lon, tags


st.header("Trip Planner")

lat, lon, _ = geocoder("Copenhagen")
print(geocoder("Copenhagen"))
print(find_pois(lat, lon, "Museums")[:3])