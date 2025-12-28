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

# The "High Priests" of Cinema (Kim Protocol Factor 2)
HEAVY_HITTERS = [
    "Kurosawa", "Bergman", "Godard", "Tarkovsky", "Kubrick", 
    "Hitchcock", "Dreyer", "Ozu", "Fellini", "Lang", 
    "Malick", "Trier", "Lynch", "Oshii", "Anno", "Kojima"
]

def log(tag, message, color=C_RESET):
    """System logging helper."""
    print(f"{color}[{tag}] {message}{C_RESET}")

# --- LOGIC LAYER (The Kim Protocol) ---
def calculate_shodan_weight(title, director, year_str, country, fmt="Digital"):
    weight = 5.0
    
    # 1. DURABILITY CHECK (Age)
    try:
        year = int(year_str)
        if year < 1960: weight += 2.0
        elif year < 1980: weight += 1.5
        elif year < 2000: weight += 1.0
        elif year > 2020: weight -= 1.0
    except ValueError:
        pass # Keep base weight if year is invalid

    # 2. THE HIGH PRIESTS
    # Case-insensitive check against the roster
    if any(h.lower() in director.lower() for h in HEAVY_HITTERS):
        weight += 2.0

    # 3. HAPTICS (Format)
    if "Blu-Ray" in fmt: 
        weight += 0.5

    # 4. ORIGIN BOOTSTRAP (International bias)
    if "USA" not in country and "United States" not in country:
        weight += 0.5

    # Clamp between 1.0 and 10.0
    return min(max(round(weight, 1), 1.0), 10.0)

# --- NETWORK LAYER ---
def fetch_movie_data(title):
    """Queries the OMDb API for raw data."""
    if not API_KEY:
        return None

    base_url = "http://www.omdbapi.com/?"
    params = urllib.parse.urlencode({'t': title, 'apikey': API_KEY})
    url = base_url + params
    
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            if data.get('Response') == 'True':
                return data
            else:
                log("API ERROR", data.get('Error', 'Unknown Error'), C_RED)
                return None
    except Exception as e:
        log("CONNECTION FAILURE", str(e), C_RED)
        return None

def load_local_ark():
    """Loads the local JSON database."""
    if os.path.exists(CANON_FILE):
        try:
            with open(CANON_FILE, 'r', encoding='utf-8') as f:
                return json.load(f).get('canon', [])
        except Exception as e:
            log("ERROR", f"Corrupt Ark Database: {e}", C_RED)
            return []
    return []

# --- MAIN LOOP ---
def main():
    # 1. System Check
    online_mode = False
    print("-" * 50)
    if API_KEY:
        log("SYSTEM", "SHODAN UPLINK: CONNECTED TO OMDb", C_GREEN)
        online_mode = True
    else:
        log("SYSTEM", "SHODAN UPLINK: OFFLINE MODE", C_RED)
        print(f"{C_YELLOW}[TIP] Export Key: export OMDB_API_KEY='your_key'{C_RESET}")

    # 2. Load Memory
    canon = load_local_ark()
    log("STATUS", f"Local Ark Loaded: {len(canon)} Artifacts", C_CYAN)
    print("-" * 50)
    
    # 3. Interactive Loop
    while True:
        try:
            query = input(f"{C_CYAN}>> SEARCH GLOBAL DATABASE: {C_RESET}").strip()
        except KeyboardInterrupt:
            print("\n")
            log("SYSTEM", "DISCONNECTING...", C_RED)
            break

        if query.lower() in ['exit', 'quit']:
            break
        
        if not online_mode:
            log("ERROR", "Uplink Down. Enable API Key to search.", C_RED)
            continue

        # Fetch & Process
        data = fetch_movie_data(query)
        if data:
            title = data.get('Title', 'Unknown')
            director = data.get('Director', 'Unknown')
            year = data.get('Year', '0000')[:4]
            country = data.get('Country', 'Unknown')
            
            # Display Data
            print(f"\n{C_GREEN}/// DATA RETRIEVED ///{C_RESET}")
            print(f"   TITLE:    {title}")
            print(f"   DIRECTOR: {director}")
            print(f"   YEAR:     {year}")
            print(f"   ORIGIN:   {country}")
            
            # Run Algorithm
            weight = calculate_shodan_weight(title, director, year, country)
            print(f"   WEIGHT:   {C_YELLOW}{weight} / 10.0{C_RESET}")
            
            # Check for Duplicates
            if any(x['title'] == title for x in canon):
                log("STATUS", "ARTIFACT ALREADY SECURED IN ARK.", C_GREEN)
            else:
                if weight > 8.0:
                    log("VERDICT", "HIGH VALUE TARGET. CONSIDER ACQUISITION.", C_GREEN)
                elif weight < 5.0:
                    log("VERDICT", "SLOP. IGNORE.", C_RED)

if __name__ == "__main__":
    main()