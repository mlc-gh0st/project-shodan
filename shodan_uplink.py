import json
import urllib.request
import urllib.parse
import os
import sys

# --- CONFIGURATION & CONSTANTS ---
API_KEY = os.getenv("OMDB_API_KEY")
CANON_FILE = "canon.json"

# ANSI Colors for Terminal UI
C_RESET  = "\033[0m"
C_RED    = "\033[31m"
C_GREEN  = "\033[32m"
C_CYAN   = "\033[36m"
C_YELLOW = "\033[33m"

# 1. THE SACRED CANON (Manual Overrides)
# These objects are too important to trust to an algorithm.
SACRED_CANON = {
    "whatever happened to robot jones?": 8.0,
    "jet set radio": 8.5,
    "tekken 3": 9.0,
    "metal gear solid 2: sons of liberty": 10.0,
    "metal gear solid 2": 10.0,
    "sonic adventure 2": 8.0,
    "akira": 10.0,
    "ghost in the shell": 9.5
}

# 2. THE HIGH PRIESTS (Architects of the Canon)
HEAVY_HITTERS = [
    "Kurosawa", "Bergman", "Godard", "Tarkovsky", "Kubrick", 
    "Hitchcock", "Dreyer", "Ozu", "Fellini", "Lang", 
    "Malick", "Trier", "Lynch", "Oshii", "Anno", "Kojima",
    "Wachowski", "Sega", "Team Silent", "Namco", "Cronenberg",
    "Gibson"
]

# 3. RESONANCE KEYS (Thematic Triggers)
# If the plot or genre vibrates with these frequencies, boost the signal.
RESONANCE_KEYS = {
    "Cyberpunk": 1.5,
    "Dystopia": 1.0,
    "Surreal": 1.0,
    "Animation": 0.5,
    "Cult": 1.0,
    "Hacker": 1.5,
    "Robot": 1.0,
    "Philosophy": 1.0,
    "Noir": 0.5
}

def log(tag, message, color=C_RESET):
    print(f"{color}[{tag}] {message}{C_RESET}")

# --- LOGIC LAYER (The Kim Protocol) ---
def calculate_shodan_weight(title, director, year_str, country, fmt="Digital", genre="", plot=""):
    # 0. SACRED CHECK (Override)
    if title.lower() in SACRED_CANON:
        return SACRED_CANON[title.lower()]

    weight = 5.0
    
    # 1. DURABILITY CHECK (Age)
    try:
        year = int(year_str)
        if year < 1960: weight += 2.0
        elif year < 1980: weight += 1.5
        elif year < 2000: weight += 1.0 # The Golden Era (90s)
        elif year > 2020: weight -= 1.0
    except ValueError:
        pass 

    # 2. THE HIGH PRIESTS
    if any(h.lower() in director.lower() for h in HEAVY_HITTERS):
        weight += 2.0

    # 3. RESONANCE PROTOCOL (Thematic Match)
    # We check both Genre and Plot for our keywords
    content_signal = (genre + " " + plot).lower()
    
    # We stack resonance, but cap the bonus so it doesn't break the scale
    for key, value in RESONANCE_KEYS.items():
        if key.lower() in content_signal:
            weight += value
            # Hard cap for resonance bonuses to prevent overflow
            if weight >= 9.5: break

    # 4. HAPTICS (Format)
    if "Blu-Ray" in fmt: 
        weight += 0.5

    # 5. ORIGIN BOOTSTRAP
    if "USA" not in country and "United States" not in country:
        weight += 0.5

    return min(max(round(weight, 1), 1.0), 10.0)

# --- NETWORK LAYER ---
def fetch_movie_data(title):
    if not API_KEY: return None
    base_url = "http://www.omdbapi.com/?"
    # We ask for 'short' plot to keep data light
    params = urllib.parse.urlencode({'t': title, 'apikey': API_KEY})
    try:
        with urllib.request.urlopen(base_url + params) as r:
            data = json.loads(r.read().decode())
            return data if data.get('Response') == 'True' else None
    except: return None

def load_local_ark():
    if os.path.exists(CANON_FILE):
        try:
            with open(CANON_FILE, 'r', encoding='utf-8') as f:
                return json.load(f).get('canon', [])
        except: return []
    return []

# --- MAIN LOOP ---
def main():
    online_mode = False
    print("-" * 50)
    if API_KEY:
        log("SYSTEM", "SHODAN UPLINK: CONNECTED TO OMDb", C_GREEN)
        online_mode = True
    else:
        log("SYSTEM", "SHODAN UPLINK: OFFLINE MODE", C_RED)
        print(f"{C_YELLOW}[TIP] Export Key: export OMDB_API_KEY='your_key'{C_RESET}")

    canon = load_local_ark()
    log("STATUS", f"Local Ark Loaded: {len(canon)} Artifacts", C_CYAN)
    print("-" * 50)
    
    while True:
        try:
            query = input(f"{C_CYAN}>> SEARCH GLOBAL DATABASE: {C_RESET}").strip()
        except KeyboardInterrupt:
            print("\n"); log("SYSTEM", "DISCONNECTING...", C_RED); break

        if query.lower() in ['exit', 'quit']: break
        
        # Check Sacred Canon first (works offline)
        if query.lower() in SACRED_CANON:
            print(f"\n{C_GREEN}/// SACRED TEXT IDENTIFIED ///{C_RESET}")
            print(f"   TITLE:    {query.title()}")
            print(f"   STATUS:   HARDCODED")
            print(f"   WEIGHT:   {C_GREEN}{SACRED_CANON[query.lower()]} / 10.0{C_RESET}")
            continue

        if not online_mode:
            log("ERROR", "Uplink Down. Enable API Key to search.", C_RED)
            continue

        data = fetch_movie_data(query)
        if data:
            title = data.get('Title', 'Unknown')
            director = data.get('Director', 'Unknown')
            year = data.get('Year', '0000')[:4]
            country = data.get('Country', 'Unknown')
            genre = data.get('Genre', '')
            plot = data.get('Plot', '')
            
            print(f"\n{C_GREEN}/// DATA RETRIEVED ///{C_RESET}")
            print(f"   TITLE:    {title}")
            print(f"   DIRECTOR: {director}")
            print(f"   YEAR:     {year}")
            print(f"   GENRE:    {genre}")
            
            weight = calculate_shodan_weight(title, director, year, country, "Digital", genre, plot)
            w_color = C_GREEN if weight > 8.0 else (C_YELLOW if weight > 5.0 else C_RED)
            print(f"   WEIGHT:   {w_color}{weight} / 10.0{C_RESET}")
            
            if any(x['title'] == title for x in canon):
                log("STATUS", "ARTIFACT ALREADY SECURED IN ARK.", C_GREEN)
            else:
                if weight > 8.0:
                    log("VERDICT", "HIGH RESONANCE. ACQUIRE.", C_GREEN)
                elif weight < 5.0:
                    log("VERDICT", "LOW SIGNAL. IGNORE.", C_RED)

if __name__ == "__main__":
    main()