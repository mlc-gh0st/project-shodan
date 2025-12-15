import json
import urllib.request
import urllib.parse
import os

# CONFIGURATION
# Replace 'YOUR_KEY_HERE' with the key sent to your email
API_KEY = "ed27c716" 
CANON_FILE = "canon.json"

# --- THE KIM PROTOCOL (Logic Layer) ---
def calculate_weight(title, director, year_str, country, fmt="Digital"):
    weight = 5.0
    
    # 1. DURABILITY (Age)
    try:
        year = int(year_str)
        if year < 1960: weight += 2.0
        elif year < 1980: weight += 1.5
        elif year < 2000: weight += 1.0
        elif year > 2020: weight -= 1.0
    except:
        pass

    # 2. THE HIGH PRIESTS
    heavy_hitters = ["Kurosawa", "Bergman", "Godard", "Tarkovsky", "Kubrick", "Hitchcock", "Dreyer", "Ozu", "Fellini", "Lang", "Malick", "Trier", "Lynch", "Oshii", "Anno", "Kojima"]
    for heavy in heavy_hitters:
        if heavy.lower() in director.lower():
            weight += 2.0
            break

    # 3. HAPTICS (Format)
    if "Blu-Ray" in fmt: weight += 0.5

    # 4. ORIGIN BOOTSTRAP
    if "USA" not in country and "United States" not in country:
        weight += 0.5

    return min(max(round(weight, 1), 1.0), 10.0)

def fetch_movie_data(title):
    """Calls the OMDb API to get the Truth."""
    if API_KEY == "YOUR_KEY_HERE":
        print("[ERROR] API Key Missing. Edit the script to add your key.")
        return None

    base_url = "http://www.omdbapi.com/?"
    params = urllib.parse.urlencode({'t': title, 'apikey': API_KEY})
    url = base_url + params
    
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            if data['Response'] == 'True':
                return data
            else:
                print(f"[API ERROR] {data['Error']}")
                return None
    except Exception as e:
        print(f"[CONNECTION FAILURE] {e}")
        return None

def load_canon():
    if os.path.exists(CANON_FILE):
        with open(CANON_FILE, 'r', encoding='utf-8') as f:
            return json.load(f).get('canon', [])
    return []

def main():
    print("/// SHODAN UPLINK: CONNECTED TO OMDb ///")
    canon = load_canon()
    print(f"[STATUS] Local Ark Loaded: {len(canon)} Artifacts.")
    
    while True:
        print("-" * 50)
        query = input(">> SEARCH GLOBAL DATABASE: ").strip()
        if query.lower() in ['exit', 'quit']: break
        
        # 1. FETCH REALITY
        data = fetch_movie_data(query)
        
        if data:
            title = data.get('Title')
            director = data.get('Director')
            year = data.get('Year')[:4] # Clean the year
            country = data.get('Country')
            
            print(f"\n[DATA RETRIEVED]")
            print(f"   TITLE:    {title}")
            print(f"   DIRECTOR: {director}")
            print(f"   YEAR:     {year}")
            print(f"   ORIGIN:   {country}")
            
            # 2. RUN KIM PROTOCOL
            weight = calculate_weight(title, director, year, country)
            print(f"   SHODAN WEIGHT: {weight} / 10.0")
            
            # 3. CHECK ARK
            peers = [x for x in canon if abs(x['shodan_weight'] - weight) < 0.2]
            
            # 4. JUDGMENT
            if any(x['title'] == title for x in canon):
                print("   [STATUS] ARTIFACT ALREADY SECURED IN ARK.")
            else:
                if weight > 8.0:
                    print("   [VERDICT] HIGH VALUE TARGET. CONSIDER ACQUISITION.")
                elif weight < 5.0:
                    print("   [VERDICT] SLOP. IGNORE.")
                
                if peers:
                    print("   [PEERS] Similar weight to:")
                    for p in peers[:2]:
                        print(f"   * {p['title']} ({p['year']})")

if __name__ == "__main__":
    main()