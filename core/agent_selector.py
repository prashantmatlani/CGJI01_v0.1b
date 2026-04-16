

# AGENT SELECTOR - core/agent_selector.py

"""
LLM-Based Agent Selector - If no rule fires, we send the input to the LLM with a prompt asking which agent should respond
"""

from core.llm_client import ask_llm
from core.agent_triggers import RULE_TRIGGERS

def rule_based_selection(user_input):
    for agent, keywords in RULE_TRIGGERS.items():
        for keyword in keywords:
            if keyword.lower() in user_input.lower():
                return agent  # Immediate match
    return None  # No rule match

def llm_based_selection(user_input):
    prompt = f"""
    Based on the user's input, which agent should respond?
    The user says: "{user_input}"

    Options: dream, shadow, myth, epistemic, bpsy, jred.
    Choose the most relevant agent and justify your choice.
    Respond with only the agent name.
    """
    response = ask_llm(prompt)
    return response.strip().lower()