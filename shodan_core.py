# shodan_core.py
# THE LOGOS: The immutable logic of the Ark.
import re

# 1. THE SACRED CANON
SACRED_CANON = {
    # --- THE GAMES (Title Trust Only) ---
    "jet set radio": {"weight": 8.5},
    "tekken 3": {"weight": 9.0},
    "metal gear solid 2: sons of liberty": {"weight": 10.0},
    "metal gear solid 2": {"weight": 10.0},
    "sonic adventure 2": {"weight": 8.0},
    
    # --- THE ANIME/TV (Strict Metadata Enforcement) ---
    "whatever happened to robot jones?": {
        "weight": 8.0, 
        "year": "2002", 
        "director": "Greg Miller" 
    },
    "akira": {
        "weight": 10.0, 
        "year": "1988", 
        "director": "Katsuhiro" 
    },
    "ghost in the shell": {
        "weight": 9.5, 
        "year": "1995", 
        "director": "Oshii" 
    },
    "cowboy bebop": {
        "weight": 10.0, 
        "year": "1998", 
        "director": "Watanabe" 
    }
}

# 2. THE APOCRYPHA
APOCRYPHA = {
    "haunting ground": "SIMULACRUM ARTIFACT (G4TV ARCHIVE)",
    "rule of rose": "SIMULACRUM ARTIFACT (PS2 MYTHOS)",
    "illbleed": "SIMULACRUM ARTIFACT (DREAMCAST CULT)",
    "michigan: report from hell": "SIMULACRUM ARTIFACT (SUDA51 ECHO)"
}

# 3. THE HIGH PRIESTS
HEAVY_HITTERS = [
    "Kurosawa", "Bergman", "Godard", "Tarkovsky", "Kubrick", 
    "Hitchcock", "Dreyer", "Ozu", "Fellini", "Lang", 
    "Malick", "Trier", "Lynch", "Oshii", "Anno", "Kojima",
    "Wachowski", "Sega", "Team Silent", "Namco", "Cronenberg",
    "Gibson", "Cameron", "Verhoeven", 
    "Madhouse", "Kawajiri", "Koike", "Watanabe",
    "Villeneuve", "Nolan", "Miller", "Refn"
]

# 4. THE TEKTONS
TEKTONS = [
    "Ryan Gosling", "Keanu Reeves", "Tom Hardy", 
    "Christian Bale", "Scarlett Johansson", "Willem Dafoe",
    "Tilda Swinton", "Mads Mikkelsen", "Jake Gyllenhaal",
    "Song Kang-ho", "Takeshi Kitano"
]

# 5. RESONANCE KEYS
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
    "Car": 0.5, "Hand-Drawn": 1.5,
    "Jazz": 1.5, "Space Western": 1.5, "Bounty Hunter": 1.0,
    "Samurai": 1.5, "Hip-Hop": 1.5, "Funk": 1.0,
    "Android": 1.5, "Hologram": 1.0, "Neon": 0.5, "Identity": 1.0,
    "Neo-Noir": 2.0,
    "Synthwave": 2.5, "Retrowave": 2.0, "Outrun": 2.0
}

def normalize_key(title):
    if not title: return ""
    return "".join(c for c in title.lower() if c.isalnum())

def get_sacred_data(title):
    """Retrieves the raw Sacred Canon data if the title matches."""
    clean_title = normalize_key(title)
    for key, data in SACRED_CANON.items():
        if normalize_key(key) == clean_title:
            return data
    return None

def check_sacred_canon(title, year=None, director=None):
    clean_title = normalize_key(title)
    
    for key, data in SACRED_CANON.items():
        if normalize_key(key) == clean_title:
            # IDENTITY CHECK
            if "year" in data:
                if not year or data["year"] not in str(year):
                    continue 
            
            if "director" in data:
                if not director or data["director"].lower() not in director.lower():
                    continue

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