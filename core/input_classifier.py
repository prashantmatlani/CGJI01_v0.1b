

# INPUT CLASSIFIER - core/input_classifier.py

def is_meaningful_input(text):

    text = text.strip().lower()

    # very short / trivial
    if len(text) < 10:
        return False

    trivial_phrases = [
        "test",
        "hello",
        "hi",
        "sample",
        "checking",
        "123"
    ]

    if any(word in text for word in trivial_phrases):
        return False

    return True