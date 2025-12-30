import json
import urllib.request
import urllib.parse
import os
import sys
# [THE SYNCHRONIZATION] Import the Soul
import shodan_core as core

# --- CONFIGURATION ---
API_KEY = os.getenv("OMDB_API_KEY")
CANON_FILE = "canon.json"

# ANSI Colors
C_RESET  = "\033[0m"
C_RED    = "\033[31m"
C_GREEN  = "\033[32m"
C_CYAN   = "\033[36m"
C_YELLOW = "\033[33m"

def log(tag, message, color=C_RESET):
    print(f"{color}[{tag}] {message}{C_RESET}")

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
            title = data.get('Title')
            
            # [CREATOR FALLBACK] 
            # If Director is N/A (common in anime), check Writer.
            director = data.get('Director', 'N/A')
            if director == "N/A":
                director = data.get('Writer', 'N/A')
                
            year = data.get('Year')[:4]
            country = data.get('Country')
            genre = data.get('Genre')
            plot = data.get('Plot')
            
            print(f"\n{C_GREEN}/// DATA RETRIEVED ///{C_RESET}")
            print(f"   TITLE:    {title}")
            print(f"   CREATOR:  {director}")
            print(f"   YEAR:     {year}")
            print(f"   GENRE:    {genre}")
            
            # [THE LOGOS] Pass data to the Core for judgment
            weight = core.calculate_shodan_weight(title, director, year, country, "Digital", genre, plot)
            
            if core.check_sacred_canon(title):
                print(f"   STATUS:   {C_CYAN}SACRED TEXT (METADATA MERGED){C_RESET}")
            
            w_color = C_GREEN if weight > 8.0 else (C_YELLOW if weight > 5.0 else C_RED)
            print(f"   WEIGHT:   {w_color}{weight} / 10.0{C_RESET}")
            
            if any(x['title'] == title for x in canon):
                log("STATUS", "ARTIFACT ALREADY SECURED IN ARK.", C_GREEN)
            else:
                if weight > 8.0: log("VERDICT", "HIGH RESONANCE. ACQUIRE.", C_GREEN)
                elif weight < 5.0: log("VERDICT", "LOW SIGNAL. IGNORE.", C_RED)

        # 3. FALLBACK (Offline or Not Found)
        else:
            sacred_weight = core.check_sacred_canon(query)
            if sacred_weight:
                print(f"\n{C_GREEN}/// SACRED TEXT IDENTIFIED (OFFLINE) ///{C_RESET}")
                print(f"   TITLE:    {query.title()}")
                print(f"   STATUS:   HARDCODED")
                print(f"   WEIGHT:   {C_GREEN}{sacred_weight} / 10.0{C_RESET}")
            elif online_mode:
                log("ERROR", "Artifact not found in Global Database.", C_RED)
            else:
                log("ERROR", "Uplink Down. Cannot verify unknown artifact.", C_RED)

if __name__ == "__main__":
    main()