import json
import urllib.request
import urllib.parse
import os
import sys
import csv
import datetime
import hashlib
import time

import shodan_core as core

# --- CONFIGURATION ---
API_KEY = os.getenv("OMDB_API_KEY")
TRAINING_FILE = "training_data.csv"

# GHOST PROTOCOL BLUE AESTHETIC
C_RESET   = "\033[0m"
C_BLUE    = "\033[34m"
C_CYAN    = "\033[36m"
C_WHITE   = "\033[37m"
C_GREEN   = "\033[32m"
C_RED     = "\033[31m"
C_GREY    = "\033[90m"

class Gatekeeper:
    def __init__(self):
        self.keys = [
            "00c3b0eb38bd4340d87219dbf8b7e289456561be9da2366b539121a22ce66512",
            "4119d857211516e53097b6928e4695e7b24d7776b772c5a2c1f038596b653999",
            "402d334057885b5d84347713d2a7625dc745c47796d67b2d2d90d7945d812e96"
        ]

    def _hash(self, token):
        return hashlib.sha256(token.strip().lower().encode()).hexdigest()

    def verify(self, raw_input):
        if "::" not in raw_input: return False
        fragments = raw_input.split("::")
        if len(fragments) != 3: return False
        return all(self._hash(f) == k for f, k in zip(fragments, self.keys))

def log(tag, message, color=C_BLUE):
    print(f"{color}[{tag}] {C_WHITE}{message}{C_RESET}")

def fetch_movie_data(title, year=None, type_=None):
    if not API_KEY: return None
    base_url = "http://www.omdbapi.com/?"
    query_params = {'t': title, 'apikey': API_KEY}
    if year: query_params['y'] = year
    if type_: query_params['type'] = type_
    
    try:
        params = urllib.parse.urlencode(query_params)
        with urllib.request.urlopen(base_url + params) as r:
            data = json.loads(r.read().decode())
            return data if data.get('Response') == 'True' else None
    except: return None

def log_training_data(title, director, year, genre, weight):
    if os.path.exists(TRAINING_FILE):
        try:
            with open(TRAINING_FILE, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) > 3:
                        if row[1].lower() == title.lower() and str(row[3]) == str(year):
                            return "DUPLICATE"
        except Exception as e:
            log("ERROR", f"READ FAILURE: {e}", C_RED)
            return "ERROR"

    try:
        with open(TRAINING_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not os.path.exists(TRAINING_FILE) or os.stat(TRAINING_FILE).st_size == 0:
                writer.writerow(['timestamp', 'title', 'director', 'year', 'genre', 'weight'])
            
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([timestamp, title, director, year, genre, weight])
            return "SUCCESS"
    except Exception as e:
        log("ERROR", f"WRITE FAILURE: {e}", C_RED)
        return "ERROR"
    
def parse_query(raw_input):
    parts = raw_input.split("::")
    title = parts[0].strip()
    year, media_type = None, None
    for part in parts[1:]:
        clean_part = part.strip().lower()
        if clean_part.isdigit(): year = clean_part
        elif clean_part in ['movie', 'series', 'episode']: media_type = clean_part
    return title, year, media_type

def main():
    online_mode = False
    security = Gatekeeper() 
    
    print(f"{C_BLUE}" + "=" * 60 + f"{C_RESET}")
    if API_KEY:
        log("GHOST_PROTOCOL", "UPLINK STABLE: OMDb CONNECTED", C_CYAN)
        online_mode = True
    else:
        log("GHOST_PROTOCOL", "OFFLINE MODE: LOCAL ENGINE ONLY", C_RED)
    print(f"{C_BLUE}" + "=" * 60 + f"{C_RESET}")
    
    while True:
        try:
            raw_input = input(f"{C_CYAN}shodan@ark:{C_BLUE}~$ {C_RESET}").strip()
        except KeyboardInterrupt:
            print("\n"); log("SYSTEM", "TERMINATING SESSION...", C_RED); break

        if raw_input.lower() in ['exit', 'quit']: break
        if not raw_input: continue

        if security.verify(raw_input):
            log("PROTOCOL", "SECRET CANON REVEALED", C_GREEN)
            continue 

        query_title, query_year, query_type = parse_query(raw_input)
        
        data = None
        if online_mode:
            search_year = query_year 
            if not search_year:
                sacred_data = core.get_sacred_data(query_title)
                if sacred_data and "year" in sacred_data:
                    search_year = sacred_data["year"]
            
            data = fetch_movie_data(query_title, search_year, query_type)

        if data:
            # --- GLOBAL SIGNAL FOUND ---
            title = data.get('Title')
            director = data.get('Director', 'N/A')
            writer = data.get('Writer', 'N/A')
            actors = data.get('Actors', 'N/A')
            raw_year = data.get('Year', '0000')
            year = raw_year[:4] if len(raw_year) >= 4 else raw_year
            country = data.get('Country', 'N/A')
            genre = data.get('Genre', 'N/A')
            plot = data.get('Plot', 'N/A')
            awards = data.get('Awards', 'N/A')
            
            print(f"\n{C_BLUE}--- ARTIFACT ANALYSIS ---{C_RESET}")
            print(f"   {C_BLUE}ID:{C_RESET}      {title} ({year})")
            print(f"   {C_BLUE}CREATOR:{C_RESET} {director}")
            print(f"   {C_BLUE}GENRE:{C_RESET}   {genre}")
            print(f"   {C_BLUE}INTEL:{C_RESET}   {C_GREY}{plot}{C_RESET}")
            
            canon_check = core.check_sacred_canon(title, year, director, writer)
            weight = 0.0
            
            if canon_check and canon_check[0] == "SACRED":
                log("STATUS", "SACRED TEXT DETECTED", C_CYAN)
                weight = float(canon_check[1])
            elif canon_check and canon_check[0] == "APOCRYPHA":
                log("STATUS", f"APOCRYPHA: {canon_check[1]}", C_GREY)
                weight = 0.0
            else:
                weight = core.calculate_shodan_weight(
                    title, director, year, country, "Digital", genre, plot, actors, awards
                )

            w_color = C_CYAN if weight > 8.0 else (C_BLUE if weight > 5.0 else C_RED)
            print(f"   {C_BLUE}WEIGHT:{C_RESET}   {w_color}{weight} / 10.0{C_RESET}")
            
            if weight >= 8.0:
                status = log_training_data(title, director, year, genre, weight)
                if status == "SUCCESS": log("MEM_BANK", "ARTIFACT ARCHIVED", C_CYAN)
        else:
            # --- FALLBACK: LOCAL ARK CHECK ---
            local_check = core.check_sacred_canon(query_title)
            if local_check:
                tag, val = local_check
                print(f"\n{C_BLUE}--- LOCAL ARK FALLBACK ---{C_RESET}")
                print(f"   {C_BLUE}ID:{C_RESET}      {query_title.upper()}")
                if tag == "SACRED":
                    log("STATUS", "SACRED TEXT IDENTIFIED (OFFLINE)", C_CYAN)
                    print(f"   {C_BLUE}WEIGHT:{C_RESET}   {C_CYAN}{val} / 10.0{C_RESET}")
                else:
                    log("STATUS", f"APOCRYPHA: {val}", C_GREY)
                    print(f"   {C_BLUE}WEIGHT:{C_RESET}   {C_GREY}0.0 / 10.0{C_RESET}")
            else:
                log("ERROR", "SIGNAL LOST: ARTIFACT NOT IN GLOBAL OR LOCAL ARK", C_RED)

if __name__ == "__main__":
    main()