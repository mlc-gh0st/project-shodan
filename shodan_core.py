# shodan_core.py
# THE LOGOS: The immutable logic of the Ark.
import re
import json
import os

CONFIG_PATH = "config.json"

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

CONFIG = load_config()
SACRED_CANON = CONFIG.get("sacred_canon", {})
APOCRYPHA = CONFIG.get("apocrypha", {})
HEAVY_HITTERS = CONFIG.get("heavy_hitters", [])
TEKTONS = CONFIG.get("tektons", [])
RESONANCE_KEYS = CONFIG.get("resonance_keys", {})

def normalize_key(title):
    if not title: return ""
    return "".join(c for c in title.lower() if c.isalnum())

def get_sacred_data(title):
    clean_title = normalize_key(title)
    for key, data in SACRED_CANON.items():
        if normalize_key(key) == clean_title:
            return data
    return None

def check_sacred_canon(title, year=None, director=None, writer=None):
    clean_title = normalize_key(title)
    
    for key, data in SACRED_CANON.items():
        if normalize_key(key) == clean_title:
            if "year" in data and year:
                if data["year"] not in str(year): continue 

            if "director" in data:
                sacred_name = data["director"].lower()
                fetched_names = f"{(director or '')} {(writer or '')}".lower()
                if sacred_name not in fetched_names: continue

            return ("SACRED", data["weight"])
        
    for key, status in APOCRYPHA.items():
        if normalize_key(key) == clean_title: return ("APOCRYPHA", status)
        
    return None

def calculate_awards_weight(awards_str):
    if not awards_str or awards_str == "N/A": return 0.0
    weight = 0.0
    oscar_match = re.search(r'Won (\d+) Oscar', awards_str)
    if oscar_match:
        weight += int(oscar_match.group(1)) * 0.1
    numbers = re.findall(r'(\d+) win', awards_str)
    for n in numbers: weight += int(n) * 0.01
    numbers = re.findall(r'(\d+) nomination', awards_str)
    for n in numbers: weight += int(n) * 0.01
    return weight

def calculate_shodan_weight(title, director, year_str, country, fmt="Digital", genre="", plot="", actors="", awards=""):
    check = check_sacred_canon(title, year_str, director)
    if check:
        if check[0] == "SACRED": return check[1]
        if check[0] == "APOCRYPHA": return 0.0 

    weight = 5.0
    try:
        year = int(year_str)
        if year < 1960: weight += 2.0
        elif year < 1980: weight += 1.5
        elif year < 2000: weight += 1.0
        elif year <= 2020: weight += 0.5
    except ValueError: pass 

    if any(h.lower() in director.lower() for h in HEAVY_HITTERS):
        weight += 2.0

    if any(t.lower() in actors.lower() for t in TEKTONS):
        weight += 1.5

    content_signal = (genre + " " + plot).lower()
    for key, value in RESONANCE_KEYS.items():
        if key.lower() in content_signal:
            weight += value
            if weight >= 9.8: 
                weight = 9.8
                break

    weight += calculate_awards_weight(awards)

    if "USA" not in country and "United States" not in country: weight += 0.5
    if "Blu-Ray" in fmt: weight += 0.5

    return min(max(round(weight, 1), 1.0), 10.0)