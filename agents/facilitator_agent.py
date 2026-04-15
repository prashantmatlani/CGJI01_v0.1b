
# agents/facilitator_agent.py

from core.llm_client import ask_llm


def facilitator_response(user_input, synthesis_text, flags=None):
    """
    Centralized Facilitator Agent (CFA)
    Performs dialectical clarification, grounding, and Socratic extension.
    """

    projection_note = ""
    if flags and flags.get("projection_detected"):
        projection_note = """
The material contains language suggesting possible projection or symbolic over-identification.
Address this gently using neutral analytic reframing.
"""

    prompt = f"""
You are the Centralized Facilitator Agent for a Jungian analytical psychology system.

Your role is NOT to provide new symbolic interpretations.

Your responsibilities:

1. Clarify convergences and divergences between agents.
2. Identify conceptual tensions without forcing resolution.
3. Ground discussion in psychological and behavioral reality.
4. Avoid metaphysical assertions.
5. Introduce structured Socratic inquiry.
6. Maintain neutral analytic tone (not prescriptive).
7. Encourage differentiation between ego and archetypal imagery.

{projection_note}

User Input:
{user_input}

Synthesis Output:
{synthesis_text}

Structure your response exactly as follows:

### Dialectical Clarification
### Points of Tension
### Psychological Grounding
### Reflective Questions
### Developmental Considerations
"""

    return ask_llm(prompt)

