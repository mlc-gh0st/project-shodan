import json
import urllib.request
import urllib.parse
import os
import sys
import csv
import datetime
import shodan_core as core

# --- CONFIGURATION ---
API_KEY = os.getenv("OMDB_API_KEY")
CANON_FILE = "canon.json"
TRAINING_FILE = "training_data.csv"

# ANSI Colors
C_RESET  = "\033[0m"
C_RED    = "\033[31m"
C_GREEN  = "\033[32m"
C_CYAN   = "\033[36m"
C_YELLOW = "\033[33m"
C_MAGENTA = "\033[35m" 
C_GREY   = "\033[90m"

def log(tag, message, color=C_RESET):
    print(f"{color}[{tag}] {message}{C_RESET}")

def fetch_movie_data(title, year=None, type_=None):
    if not API_KEY: return None
    base_url = "http://www.omdbapi.com/?"
    
    # [THE LOGOS] Construct Query
    query_params = {'t': title, 'apikey': API_KEY}
    if year: query_params['y'] = year
    if type_: query_params['type'] = type_
        
    params = urllib.parse.urlencode(query_params)
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

def log_training_data(title, director, year, genre, weight):
    """
    Logs data to CSV only if it is not already present.
    Returns: "SUCCESS", "DUPLICATE", or "ERROR"
    """
    file_exists = os.path.exists(TRAINING_FILE)
    
    # 1. READ CHECK (The Recall)
    if file_exists:
        try:
            with open(TRAINING_FILE, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    # CSV Format: [timestamp, title, director, year, genre, weight]
                    # We check if Title and Year match to avoid duplicates
                    if len(row) > 3:
                        existing_title = row[1]
                        existing_year = row[3]
                        if existing_title.lower() == title.lower() and str(existing_year) == str(year):
                            return "DUPLICATE"
        except Exception: 
            return "ERROR"

    # 2. WRITE ACTION (The Inscription)
    try:
        with open(TRAINING_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['timestamp', 'title', 'director', 'year', 'genre', 'weight'])
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([timestamp, title, director, year, genre, weight])
            return "SUCCESS"
    except Exception: 
        return "ERROR"

def parse_query(raw_input):
    """
    Parses 'Title :: Year :: Type' syntax.
    Returns (title, year, type)
    """
    parts = raw_input.split("::")
    title = parts[0].strip()
    year = None
    media_type = None

    # Analyze additional segments
    for part in parts[1:]:
        clean_part = part.strip().lower()
        if clean_part.isdigit():
            year = clean_part
        elif clean_part in ['movie', 'series', 'episode']:
            media_type = clean_part
            
    return title, year, media_type

def main():
    online_mode = False
    print("-" * 60)
    if API_KEY:
        log("SYSTEM", "SHODAN UPLINK: CONNECTED TO OMDb", C_GREEN)
        online_mode = True
    else:
        log("SYSTEM", "SHODAN UPLINK: OFFLINE MODE", C_RED)
    
    canon = load_local_ark()
    log("STATUS", f"Local Ark Loaded: {len(canon)} Artifacts", C_CYAN)
    print("-" * 60)
    
    while True:
        try:
            raw_input = input(f"{C_CYAN}>> SEARCH GLOBAL DATABASE: {C_RESET}").strip()
        except KeyboardInterrupt:
            print("\n"); log("SYSTEM", "DISCONNECTING...", C_RED); break

        if raw_input.lower() in ['exit', 'quit']: break
        if not raw_input: continue

        # [SEMANTIC PARSING]
        query_title, query_year, query_type = parse_query(raw_input)
        
        if query_year or query_type:
            log("SYSTEM", f"MANUAL OVERRIDE DETECTED. YEAR: {query_year} | TYPE: {query_type}", C_YELLOW)

        # 1. ATTEMPT UPLINK
        data = None
        if online_mode:
            search_year = query_year 

            # [PRE-COGNITION] Sacred Override (Only if no manual year set)
            if not search_year:
                sacred_data = core.get_sacred_data(query_title)
                if sacred_data and "year" in sacred_data:
                    search_year = sacred_data["year"]
                    log("SYSTEM", f"SACRED OVERRIDE ENGAGED. TARGETING YEAR: {search_year}", C_YELLOW)
            
            # Execute Interrogation
            data = fetch_movie_data(query_title, search_year, query_type)

        # 2. PROCESS SIGNAL
        if data:
            title = data.get('Title')
            director = data.get('Director', 'N/A')
            writer = data.get('Writer', 'N/A')
            actors = data.get('Actors', 'N/A')
            raw_year = data.get('Year', '0000')
            year = raw_year[:4] if len(raw_year) >= 4 else raw_year
            country = data.get('Country')
            genre = data.get('Genre')
            plot = data.get('Plot', 'N/A')
            awards = data.get('Awards', 'N/A')
            m_type = data.get('Type', 'N/A')
            
            # [DISPLAY THE TABLE]
            print(f"\n{C_GREEN}/// DATA RETRIEVED ({m_type.upper()}) ///{C_RESET}")
            print(f"   TITLE:    {title}")
            print(f"   YEAR:     {year}")
            print(f"   CREATOR:  {director}")
            print(f"   WRITER:   {writer}")
            print(f"   ACTORS:   {actors}")
            print(f"   GENRE:    {genre}")
            print(f"   AWARDS:   {awards}")
            print(f"   PLOT:     {C_GREY}{plot}{C_RESET}")
            
            # [THE LOGOS] Check Status
            canon_check = core.check_sacred_canon(title, year, director)
            
            if canon_check and canon_check[0] == "APOCRYPHA":
                print(f"   STATUS:   {C_MAGENTA}/// {canon_check[1]} ///{C_RESET}")
                print(f"   NOTE:     Object exists in the Simulacrum but not the Ark.")
                
            else:
                weight = core.calculate_shodan_weight(
                    title, director, year, country, "Digital", genre, plot, actors, awards
                )
                
                if canon_check and canon_check[0] == "SACRED":
                    print(f"   STATUS:   {C_CYAN}SACRED TEXT (METADATA MERGED){C_RESET}")
                
                w_color = C_GREEN if weight > 8.0 else (C_YELLOW if weight > 5.0 else C_RED)
                print(f"   WEIGHT:   {w_color}{weight} / 10.0{C_RESET}")
                
                # [THE MEMORY] Check for Duplicates
                if weight >= 8.0:
                    status = log_training_data(title, director, year, genre, weight)
                    if status == "SUCCESS":
                        log("MEMORY", "ARTIFACT SAVED TO TRAINING DATA.", C_GREEN)
                    elif status == "DUPLICATE":
                        log("MEMORY", "ARTIFACT ALREADY IN TRAINING DATA. SKIPPING.", C_YELLOW)
                    else:
                        log("ERROR", "MEMORY WRITE FAILED.", C_RED)
                
                if any(x['title'] == title for x in canon):
                    log("STATUS", "ARTIFACT ALREADY SECURED IN ARK.", C_GREEN)
                else:
                    if weight > 8.0: log("VERDICT", "HIGH RESONANCE. ACQUIRE.", C_GREEN)
                    elif weight < 5.0: log("VERDICT", "LOW SIGNAL. IGNORE.", C_RED)

        else:
            # Fallback
            canon_check = core.check_sacred_canon(query_title)
            if canon_check:
                if canon_check[0] == "APOCRYPHA":
                    print(f"\n{C_MAGENTA}/// APOCRYPHA IDENTIFIED ///{C_RESET}")
                    print(f"   TITLE:    {query_title.title()}")
                    print(f"   STATUS:   {canon_check[1]}")
                else:
                    print(f"\n{C_GREEN}/// SACRED TEXT IDENTIFIED (OFFLINE) ///{C_RESET}")
                    print(f"   TITLE:    {query_title.title()}")
                    print(f"   STATUS:   HARDCODED")
                    print(f"   WEIGHT:   {C_GREEN}{canon_check[1]} / 10.0{C_RESET}")
            elif online_mode:
                log("ERROR", "Artifact not found in Global Database.", C_RED)
            else:
                log("ERROR", "Uplink Down.", C_RED)

if __name__ == "__main__":
    main()