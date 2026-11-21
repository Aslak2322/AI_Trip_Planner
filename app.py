import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv
import requests

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

def geocoder(city):
    r = requests.get(
        NOVATIM_URL,
        params={"q": city_names, "format": "json", "limit": 1},
        headers=headers,
        timeout=15
    )
    if r.status_code != 200:
        return None                       # server error, rate limit, etc.
    results = r.json()
    if not results:
        return None                       # nothing found
    top = results[0]
    return float(top["lat"]), float(top["lon"]), top["display_name"]

CATEGORIES = {
    "Restaurants": ("amenity", "restaurant"),
    "Cafés":       ("amenity", "cafe"),
    "Museums":     ("tourism", "museum"),
    "Parks":       ("leisure", "park"),
    "Attractions": ("tourism", "attraction"),
}

def find_pois(lat, lon, category, radius=1000, limit=20):
    key, value = CATEGORIES[category]
    query = f"""
    [out:json][timeout:30];
    nwr["{key}"="{value}"]["name"](around:{radius},{lat},{lon});
    out center {limit};
    """

    r = requests.get(
        OVERPASS_URL,
        data={"data": query},
        headers=headers,
    )
    if r.status_code != 200:
        return None
    results = r.json()
    if not results:
        return None
    top = results[0]
    return 
    # POST it with headers=HEADERS and timeout=30, check status_code,
    # then loop over "elements" and return a list of dicts with name, lat, lon, tags


st.header("Trip Planner")