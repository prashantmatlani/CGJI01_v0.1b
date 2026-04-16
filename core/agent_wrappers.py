

# AGENT WRAPPERS - core/agent_wrappers.py

from agents.jung_agent import jung_agent
#from agents.dream_agent import dream_agent, dream_interpret
from agents.dream_agent import dream_interpret

# -----------------------------
# JUNG WRAPPER
# -----------------------------
def jung_response(text):

    state = {
        "original_query": text,
        "conversation": [],
        "last_user_input": text
    }

    result = jung_agent(state)

    # 🔥 FIX
    if isinstance(result, dict):
        #return result.get("message", "No response from Jung agent")
        return result.get("content", "No response from Jung agent")

    return result

# -----------------------------
# DREAM WRAPPER
# -----------------------------
def dream_response(text):

    state = {
        "original_query": text,
        "conversation": [],
        "last_user_input": text
    }

    result = dream_interpret(state)

    # 🔥 FIX
    if isinstance(result, dict):
        #return result.get("message", "No response from Dream agent")
        return result.get("content", "No response from Dream agent")

    return result