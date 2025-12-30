import json
import urllib.request
import urllib.parse
import os
import sys

# --- CONFIGURATION & CONSTANTS ---
API_KEY = os.getenv("OMDB_API_KEY")
CANON_FILE = "canon.json"

# ANSI Colors
C_RESET  = "\033[0m"
C_RED    = "\033[31m"
C_GREEN  = "\033[32m"
C_CYAN   = "\033[36m"
C_YELLOW = "\033[33m"

# 1. THE SACRED CANON
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

# 2. THE HIGH PRIESTS
HEAVY_HITTERS = [
    "Kurosawa", "Bergman", "Godard", "Tarkovsky", "Kubrick", 
    "Hitchcock", "Dreyer", "Ozu", "Fellini", "Lang", 
    "Malick", "Trier", "Lynch", "Oshii", "Anno", "Kojima",
    "Wachowski", "Sega", "Team Silent", "Namco", "Cronenberg",
    "Gibson", "Cameron", "Verhoeven", 
    "Madhouse", "Kawajiri", "Koike" # The Redline Architect
]

# 3. RESONANCE KEYS (Thematic Triggers)
# [UPDATED] Added Racing / Velocity / Tournament Tokens
RESONANCE_KEYS = {
    "Cyberpunk": 1.5, "Dystopia": 1.0, "Surreal": 1.0,
    "Animation": 0.5, "Cult": 1.0, "Hacker": 1.5,
    "Robot": 1.0, "Philosophy": 1.0, "Noir": 0.5,
    "Tech-Noir": 2.0, "Cyborg": 1.5, "Time Travel": 1.0,
    "Artificial Intelligence": 1.5, "AI": 1.0,
    "Mars": 1.0, "Memory": 1.0, "Virtual Reality": 1.5, 
    "Simulation": 1.5, "Dream": 0.5,
    "Vampire": 1.5, "Gothic": 1.5, "Post-Apocalyptic": 1.5,
    "Hunter": 0.5, "Occult": 1.0, "Demon": 1.0,
    "Racing": 2.0, "Speed": 1.0, "Tournament": 1.0, 
    "Car": 0.5, "Hand-Drawn": 1.5
}

def log(tag, message, color=C_RESET):
    print(f"{color}[{tag}] {message}{C_RESET}")

def check_sacred_canon(title):
    if not title: return None
    clean_title = "".join(c for c in title.lower() if c.isalnum())
    for key, weight in SACRED_CANON.items():
        clean_key = "".join(c for c in key.lower() if c.isalnum())
        if clean_title == clean_key: return weight
    return None

def calculate_shodan_weight(title, director, year_str, country, fmt="Digital", genre="", plot=""):
    sacred_weight = check_sacred_canon(title)
    if sacred_weight: return sacred_weight

    weight = 5.0
    
    # 1. DURABILITY
    try:
        year = int(year_str)
        if year < 1960: weight += 2.0
        elif year < 1980: weight += 1.5
        elif year < 2000: weight += 1.0
        elif year > 2020: weight -= 1.0
    except ValueError: pass 

    # 2. HIGH PRIESTS
    if any(h.lower() in director.lower() for h in HEAVY_HITTERS):
        weight += 2.0

    # 3. RESONANCE
    content_signal = (genre + " " + plot).lower()
    for key, value in RESONANCE_KEYS.items():
        if key.lower() in content_signal:
            weight += value
            if weight >= 9.8: 
                weight = 9.8
                break

    # 4. ORIGIN & FORMAT
    if "USA" not in country and "United States" not in country: weight += 0.5
    if "Blu-Ray" in fmt: weight += 0.5

    return min(max(round(weight, 1), 1.0), 10.0)

# --- NETWORK LAYER ---
def fetch_movie_data(title):
    if not API_KEY: return None
    base_url = "http://www.omdbapi.com/?"
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

def main():
    online_mode = False
    print("-" * 50)
    if API_KEY:
        log("SYSTEM", "SHODAN UPLINK: CONNECTED TO OMDb", C_GREEN)
        online_mode = True
    else:
        log("SYSTEM", "SHODAN UPLINK: OFFLINE MODE", C_RED)
    
    canon = load_local_ark()
    log("STATUS", f"Local Ark Loaded: {len(canon)} Artifacts", C_CYAN)
    print("-" * 50)
    
    while True:
        try:
            query = input(f"{C_CYAN}>> SEARCH GLOBAL DATABASE: {C_RESET}").strip()
        except KeyboardInterrupt:
            print("\n"); log("SYSTEM", "DISCONNECTING...", C_RED); break

        if query.lower() in ['exit', 'quit']: break
        
        # 1. ATTEMPT UPLINK
        data = None
        if online_mode:
            data = fetch_movie_data(query)

        # 2. PROCESS SIGNAL
        if data:
            title = data.get('Title'); director = data.get('Director'); year = data.get('Year')[:4]
            country = data.get('Country'); genre = data.get('Genre'); plot = data.get('Plot')
            
            print(f"\n{C_GREEN}/// DATA RETRIEVED ///{C_RESET}")
            print(f"   TITLE:    {title}\n   DIRECTOR: {director}\n   YEAR:     {year}\n   GENRE:    {genre}")
            
            weight = calculate_shodan_weight(title, director, year, country, "Digital", genre, plot)
            
            if check_sacred_canon(title):
                print(f"   STATUS:   {C_CYAN}SACRED TEXT (METADATA MERGED){C_RESET}")
            
            w_color = C_GREEN if weight > 8.0 else (C_YELLOW if weight > 5.0 else C_RED)
            print(f"   WEIGHT:   {w_color}{weight} / 10.0{C_RESET}")
            
            if any(x['title'] == title for x in canon):
                log("STATUS", "ARTIFACT ALREADY SECURED IN ARK.", C_GREEN)
            else:
                if weight > 8.0: log("VERDICT", "HIGH RESONANCE. ACQUIRE.", C_GREEN)
                elif weight < 5.0: log("VERDICT", "LOW SIGNAL. IGNORE.", C_RED)

        # 3. FALLBACK
        else:
            sacred_weight = check_sacred_canon(query)
            if sacred_weight:
                print(f"\n{C_GREEN}/// SACRED TEXT IDENTIFIED (OFFLINE) ///{C_RESET}")
                print(f"   TITLE:    {query.title()}\n   STATUS:   HARDCODED")
                print(f"   WEIGHT:   {C_GREEN}{sacred_weight} / 10.0{C_RESET}")
            elif online_mode:
                log("ERROR", "Artifact not found in Global Database.", C_RED)
            else:
                log("ERROR", "Uplink Down. Cannot verify unknown artifact.", C_RED)

if __name__ == "__main__":
    main()