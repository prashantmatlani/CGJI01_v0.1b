
#MYTH AGENT — agents/myth_agent.py

from core.llm_client import ask_llm

def myth_response(text):
    prompt = f"""
Amplify this material through mythological and archetypal parallels.
"""
    return ask_llm(prompt)

