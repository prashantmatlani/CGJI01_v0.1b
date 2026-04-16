
from core.llm_client import ask_llm

def synthesize_jung_unified_agent(conversation_history):

    transcript = ""

    for entry in conversation_history:
        for role, content in entry.items():
            transcript += f"{role.upper()}: {content}\n\n"

    prompt = f"""
You are a synthesis agent for Jung Unified.

Summarize the psychological themes, insights, tensions,
and unresolved questions emerging from this dialogue.

Preserve disagreements.
Remain grounded psychologically.
Avoid metaphysical inflation.

Dialogue:
{transcript}
"""

    return ask_llm(prompt)
