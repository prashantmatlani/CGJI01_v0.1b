
#DREAM INTERPRETER — dream_engine/interpreter.py

from dream_engine.symbol_extractor import extract_symbols
from dream_engine.archetype_mapper import map_archetypes

def interpret_dream(text):
    symbols = extract_symbols(text)
    archetypes = map_archetypes(symbols)

    return {
        "symbols": symbols,
        "archetypes": archetypes
    }
