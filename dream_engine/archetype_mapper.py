
#ARCHETYPE MAPPER — dream_engine/archetype_mapper.py

ARCHETYPES = {
    "snake": "Transformation / Libido",
    "water": "Unconscious",
    "mother": "Great Mother",
    "shadow": "Repressed Psyche",
    "fire": "Renewal",
}

def map_archetypes(symbols):
    return {s: ARCHETYPES.get(s, "Unknown") for s in symbols}

