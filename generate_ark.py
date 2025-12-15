import csv
import json
import os

# CONFIGURATION
INPUT_FILE = "source.csv"  # This must match your converted file name
OUTPUT_FILE = "canon.json"

# --- THE HARDCODED DIGITAL CANON ---
# These are the artifacts that exist outside the spreadsheet.
DIGITAL_CANON = [
    {"title": "Akira", "director": "Otomo, Katsuhiro", "year": "1988", "type": "ANIME_CEL", "weight": 10.0, "notes": "The Nuclear Cathedral."},
    {"title": "Neon Genesis Evangelion", "director": "Anno, Hideaki", "year": "1995", "type": "ANIME_CEL", "weight": 9.5, "notes": "The AT Field / Soul Barrier."},
    {"title": "Ghost in the Shell", "director": "Oshii, Mamoru", "year": "1995", "type": "ANIME_CEL", "weight": 9.5, "notes": "The Ghost in the Machine."},
    {"title": "Cowboy Bebop", "director": "Watanabe, Shinichiro", "year": "1998", "type": "ANIME_CEL", "weight": 9.0, "notes": "The Jazz of the Void."},
    {"title": "Robot Jones", "director": "Miller, Greg", "year": "2002", "type": "ANIMATION_WESTERN", "weight": 7.5, "notes": "The Prototype of the Remnant."},
    {"title": "Angel's Egg", "director": "Oshii, Mamoru", "year": "1985", "type": "ANIME_CEL", "weight": 8.5, "notes": "Faith in the Wasteland."},
    {"title": "Tekken 3", "director": "Namco", "year": "1997", "type": "GAME_FIGHTING", "weight": 9.0, "notes": "The Frame Data of Reality."},
    {"title": "Tekken 8", "director": "Harada, Katsuhiro", "year": "2024", "type": "GAME_FIGHTING", "weight": 8.5, "notes": "The Current Battlefield. Blue Spark Protocol."},
    {"title": "Metal Gear Solid 2: Sons of Liberty", "director": "Kojima, Hideo", "year": "2001", "type": "GAME_NARRATIVE", "weight": 10.0, "notes": "Prediction of the Digital Wasteland."},
    {"title": "Silent Hill 2", "director": "Team Silent", "year": "2001", "type": "GAME_HORROR", "weight": 9.5, "notes": "The James Protocol. Trauma Audit."},
    {"title": "Sonic Adventure 2", "director": "Iizuka, Takashi", "year": "2001", "type": "GAME_DREAMCAST", "weight": 8.0, "notes": "The Tragedy of the Ark."},
    {"title": "Deus Ex", "director": "Spector, Warren", "year": "2000", "type": "GAME_SIM", "weight": 9.0, "notes": "God from the Machine."},
    {"title": "Jet Set Radio", "director": "Sega", "year": "2000", "type": "GAME_DREAMCAST", "weight": 8.5, "notes": "The Aesthetic of Rebellion."},
    {"title": "Final Fantasy VII", "director": "Kitase, Yoshinori", "year": "1997", "type": "GAME_RPG", "weight": 9.5, "notes": "Identity Crisis in the Industrial City."}
]

# THE KIM PROTOCOL WEIGHTING ALGORITHM
def calculate_shodan_weight(row):
    weight = 5.0 
    
    # Flexible column reading (handles case sensitivity)
    title = row.get('Title') or row.get('title') or ''
    director = row.get('Director') or row.get('director') or ''
    year_str = row.get('Year') or row.get('year') or '0'
    country = row.get('Country') or row.get('country') or ''
    fmt = row.get('Format') or row.get('format') or ''

    # 1. DURABILITY CHECK (Age)
    try:
        year = int(year_str)
        if year < 1960: weight += 2.0
        elif year < 1980: weight += 1.5
        elif year < 2000: weight += 1.0
        elif year > 2020: weight -= 1.0
    except:
        pass

    # 2. THE HIGH PRIESTS
    heavy_hitters = [
        "Kurosawa", "Bergman", "Godard", "Tarkovsky", "Kubrick", 
        "Hitchcock", "Dreyer", "Ozu", "Fellini", "Lang", "Malick", "Trier"
    ]
    for heavy in heavy_hitters:
        if heavy in director:
            weight += 2.0
            break

    # 3. HAPTICS (Format)
    if "Blu-Ray" in fmt:
        weight += 0.5

    # 4. ORIGIN BOOTSTRAP
    if "US" not in country:
        weight += 0.5

    return min(max(round(weight, 1), 1.0), 10.0)

def main():
    print("/// PROJECT SHODAN: ARK GENERATION ///")
    
    canon_entries = []
    
    # PHASE 1: INGEST ANALOG (The CSV)
    if os.path.exists(INPUT_FILE):
        print(f"[SYSTEM] Reading {INPUT_FILE}...")
        try:
            # utf-8-sig handles the BOM from Excel exports
            with open(INPUT_FILE, mode='r', encoding='utf-8-sig', errors='replace') as f:
                reader = csv.DictReader(f)
                
                count = 0
                for row in reader:
                    title = row.get('Title') or row.get('title')
                    if not title: continue
                    
                    weight = calculate_shodan_weight(row)
                    
                    entry = {
                        "id": f"ARCHIVE-{len(canon_entries):04d}",
                        "title": title.strip(),
                        "director": row.get('Director') or row.get('director'),
                        "year": row.get('Year') or row.get('year'),
                        "format": row.get('Format') or row.get('format'),
                        "type": "CINEMA_ANALOG",
                        "shodan_weight": weight,
                        "status": "ARCHIVED",
                        "tags": ["CRITERION"]
                    }
                    canon_entries.append(entry)
                    count += 1
            print(f"[SUCCESS] Ingested {count} Analog Artifacts.")
        except Exception as e:
            print(f"[ERROR] Failed to read CSV: {e}")
    else:
        print(f"[CRITICAL] '{INPUT_FILE}' NOT FOUND.")
        print("Please ensure you exported your Excel file to CSV and named it 'source.csv'.")
        return

    # PHASE 2: INJECT DIGITAL (Hardcoded List)
    print("[SYSTEM] Injecting Digital Canon...")
    for item in DIGITAL_CANON:
        entry = {
            "id": f"DIGITAL-{len(canon_entries):04d}",
            "title": item["title"],
            "director": item["director"],
            "year": item["year"],
            "format": "DIGITAL/ROM",
            "type": item["type"],
            "shodan_weight": item["weight"],
            "status": "ARCHIVED",
            "tags": ["KIM_PROTOCOL", "MANUAL_ENTRY"],
            "notes": item.get("notes", "")
        }
        canon_entries.append(entry)

    # OUTPUT GENERATION
    database = {
        "meta": {
            "operator": "James Leitner",
            "version": "2.0",
            "protocol": "Kim Protocol",
            "total_artifacts": len(canon_entries)
        },
        "canon": canon_entries
    }
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(database, f, indent=2)
        
    print(f"[SUCCESS] Total Database Size: {len(canon_entries)} entries.")
    print(f"[OUTPUT] Generated '{OUTPUT_FILE}'.")
    print("The Ark is sealed.")

if __name__ == "__main__":
    main()
    print("--------------------------------------------------")
    print("PROJECT SHODAN: Ark Generation Complete. Logic is Sound.")