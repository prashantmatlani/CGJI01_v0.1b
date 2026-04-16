
#SHADOW AGENT — agents/shadow_agent.py

from core.llm_client import ask_llm

def shadow_response(text):
    prompt = f"""
Analyze possible shadow elements, repression, denied traits, or unconscious conflicts.

TEXT:
{text}
"""
    return ask_llm(prompt)

