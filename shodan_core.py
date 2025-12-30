# shodan_core.py
# THE LOGOS: The immutable logic of the Ark.

# 1. THE SACRED CANON (Verified Truths)
SACRED_CANON = {
    "whatever happened to robot jones?": 8.0,
    "jet set radio": 8.5,
    "tekken 3": 9.0,
    "metal gear solid 2: sons of liberty": 10.0,
    "metal gear solid 2": 10.0,
    "sonic adventure 2": 8.0,
    "akira": 10.0,
    "ghost in the shell": 9.5,
    "cowboy bebop": 10.0
}

# 2. THE APOCRYPHA (Hidden/Shadow Canon)
# Things verified only through the Simulacrum (G4TV, Magazines, Lost Memories).
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
    "Madhouse", "Kawajiri", "Koike", "Watanabe"
]

# 4. RESONANCE KEYS
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
    "Samurai": 1.5, "Hip-Hop": 1.5, "Funk": 1.0
}

def check_sacred_canon(title):
    if not title: return None
    clean_title = "".join(c for c in title.lower() if c.isalnum())
    
    # Check Sacred Canon
    for key, weight in SACRED_CANON.items():
        clean_key = "".join(c for c in key.lower() if c.isalnum())
        if clean_title == clean_key: return ("SACRED", weight)
        
    # Check Apocrypha
    for key, status in APOCRYPHA.items():
        clean_key = "".join(c for c in key.lower() if c.isalnum())
        if clean_title == clean_key: return ("APOCRYPHA", status)
        
    return None

def calculate_shodan_weight(title, director, year_str, country, fmt="Digital", genre="", plot=""):
    # 0. SACRED/APOCRYPHA CHECK
    # This logic is now handled in the Uplink to determine display style,
    # but we keep the logic here for the calculation itself.
    check = check_sacred_canon(title)
    if check:
        if check[0] == "SACRED": return check[1]
        if check[0] == "APOCRYPHA": return 0.0 # Special handling

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