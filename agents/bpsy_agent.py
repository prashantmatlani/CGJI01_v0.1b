
from core.llm_client import ask_llm

def extract_buddhist_structure(text):
    structure = {}

    # simple heuristic detection
    if any(word in text.lower() for word in ["always", "forever", "never"]):
        structure["reification"] = True

    if any(word in text.lower() for word in ["anger", "hate", "resent"]):
        structure["aversion"] = True

    if any(word in text.lower() for word in ["desire", "want", "need"]):
        structure["craving"] = True

    if any(word in text.lower() for word in ["me", "mine", "myself"]):
        structure["self_reference"] = True

    return structure


def bpsy_response(text):

    structure = extract_buddhist_structure(text)

    prompt = f"""
You are an expert in Buddhist Literature and Psychology and Abhidharma.

Detected cognitive features:
{structure}

Analyze the psychological material using precise Buddhist theories such as - but NOT limited to - Anatta, Tilakhana, Paticcasamuppada, Alayavijnana, 
Kshanikavada (Theory of Momentariness), Kleshas, Five Aggregates, etc.

Remain structured and analytical.
"""

    return ask_llm(prompt)
