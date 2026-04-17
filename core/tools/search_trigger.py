
# ./core/search_trigger.py

def needs_web_search(user_input):
    trigger_words = [
        "what is", "who is", "define", "meaning of",
        "lookup", "search", "information on"
    ]

    user_lower = user_input.lower()

    return any(t in user_lower for t in trigger_words)
