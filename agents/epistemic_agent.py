
#EPISTEMIC AGENT — agents/epistemic_agent.py
from core.llm_client import ask_llm

def epistemic_response(text):
    prompt = f"""
Critically evaluate limits of interpretation.
Flag uncertainty, projection risks, and epistemic caution.
"""
    return ask_llm(prompt)

