
# core/intent_detector.py

def detect_intent(text: str):
    """
    Detects whether input requires full psychological analysis
    or is a system/meta/diagnostic message.
    """

    lowered = text.lower()

    diagnostic_markers = [
        "test",
        "testing",
        "system check",
        "confirm",
        "working",
        "is this working",
        "respond with",
        "just respond",
        "only confirm",
        "only a test",
        "hello",
        "hi",
        "ping"
    ]

    for marker in diagnostic_markers:
        if marker in lowered:
            return "diagnostic"

    # length heuristic (very short = not depth material)
    if len(text.split()) < 4:
        return "minimal"

    return "analysis"
