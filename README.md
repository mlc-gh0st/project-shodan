# PROJECT SHODAN // OMNI-DATABASE UPLINK

> *"The signal distorts. The machine discriminates."*

**Project Shodan** is a Python-based intelligence uplink designed to interrogate public cultural databases (OMDb, Last.fm, IGDB). The global media signal **floods** the user with recency bias and commercial echoes; Shodan **intercepts** this stream and **enforces** a strict theological hierarchy, isolating **Sacred Artifacts** from the surrounding simulacra.

It is currently active for **Film/TV** (via OMDb), with modules for **Audio** and **Interactive Media** in development.

## /// CORE OBJECTIVES

1.  **Semantic Interrogation:** The tool **bypasses** GUI ambiguity via strict command-line syntax (e.g., `Title :: Year :: Type`).
2.  **Metadata Enforcement:** The Core **rejects** modern remakes and algorithmically boosted content to protect the identity of original works (e.g., prioritizing *Ghost in the Shell* 1995 over 2017).
3.  **The Resonance Engine:** The system **evaluates** artifacts not by popularity, but by **Aesthetic Durability** (Neo-Noir, Synthwave, Cyberpunk) and **Tekton Metrics** (Key Creators).

## /// THE ARCHITECTURE

The system operates as a modular barrier against the data flood:

* **Visual Cortex (`shodan_uplink.py`):** The primary interface. **Connects** to the **OMDb API** to retrieve film and television metadata.
* **The Soul (`shodan_core.py`):** The logic kernel. **Contains** the scoring algorithms, the `RESONANCE_KEYS`, and the **Sacred Canon** definitions.
* **The Memory (`training_data.csv`):** A local, deduplicated ledger. **Archiving** only "High Resonance" artifacts (8.0+ Score) for future predictive modeling.

## /// USAGE & SYNTAX

Shodan empowers the operator to **strip** away the GUI and **interact** with data directly.

**Standard Query:**
```bash
python3 shodan_uplink.py
>> SEARCH GLOBAL DATABASE: Blade Runner 2049