
# SIGNIFICANCE DETECTION ENGINE
#core/detection_engine.py

from core.domain_triggers import *
import re

def keyword_score(text, triggers):
    score = 0
    #for word, weight in triggers.items():
    if isinstance(triggers, dict):
        iterable = triggers.items()
    else:
        iterable = [(word, 1.0) for word in triggers]

    for word, weight in iterable:

        if re.search(rf"\b{word}\b", text.lower()):
            score += weight
    return min(score, 1)

def depth_score(text):
    score = 0
    for word in DEPTH_WORDS:
        if word in text.lower():
            score += 0.2
    return min(score, 1)

def pattern_score(text):
    score = 0
    if "always" in text.lower() or "again" in text.lower():
        score += 0.3
    if "why do i" in text.lower():
        score += 0.3
    if "i keep" in text.lower():
        score += 0.3
    return min(score, 1)

def significance(text, triggers):
    semantic = keyword_score(text, triggers)
    depth = depth_score(text)
    pattern = pattern_score(text)

    return semantic*0.4 + depth*0.3 + pattern*0.3