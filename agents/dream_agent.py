
#DREAM AGENT — agents/dream_agent.py

from core.llm_client import ask_llm


#def dream_response(text):
#    prompt = f"""
#Analyze this as a dream.
#Extract symbols, emotional tone, archetypes, and unconscious themes.

#DREAM:
#{text}
#"""
#    return ask_llm(prompt)


def dream_agent(state):

    # Ask user if dream interpretation is needed
    return {
        "message": "Would you like a dream interpretation perspective on this?",
        "next": "dream_confirm"
    }


def dream_confirm(state):

    user_input = state.get("last_user_input", "").lower()

    if user_input in ["yes", "y"]:

        return {
            "message": "Please describe your dream in more detail.",
            "next": "dream_interpret"
        }

    else:
        return {
            "message": "Skipping dream perspective.",
            "next": "shadow_agent"
        }


def dream_interpret(state):

    text = state.get("original_query")

    # call LLM here
    interpretation = "Dream interpretation goes here..."

    return {
        "message": interpretation,
        "next": "shadow_agent"
    }