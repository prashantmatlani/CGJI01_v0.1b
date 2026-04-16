
#DREAM SYMBOL ENGINE — dream_engine/symbol_extractor.py

import re

COMMON_SYMBOLS = ["water", "snake", "death", "mother", "shadow", "fire", "mirror"]

def extract_symbols(text):
    found = []
    for s in COMMON_SYMBOLS:
        if re.search(rf"\b{s}\b", text.lower()):
            found.append(s)
    return found

