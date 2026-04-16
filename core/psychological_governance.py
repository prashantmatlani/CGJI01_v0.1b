
# core/psychological_governance.py

def detect_projection_markers(text):
    """
    Simple heuristic projection detection.
    Expand later with NLP scoring.
    """

    markers = [
        "always",
        "never",
        "ultimate truth",
        "they are evil",
        "I am the Self",
        "beyond ego",
        "absolute",
        "final truth"
    ]

    lowered = text.lower()

    for marker in markers:
        if marker in lowered:
            return True

    return False


def generate_flags(user_input):
    return {
        "projection_detected": detect_projection_markers(user_input)
    }
