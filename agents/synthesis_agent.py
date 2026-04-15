
#SYNTHESIS AGENT — agents/synthesis_agent.py

from core.llm_client import ask_llm

def synthesize(jung, dream, shadow, myth, epistemic, bpsy=None, jred=None):
    """
    Synthesis Agent:
    - Summarizes faithfully
    - Preserves disagreement
    - Does NOT resolve metaphysical conflicts
    """

    prompt = f"""
You are the Synthesis Agent in a Jungian multi-agent analytical system.

Your task:

1. Faithfully summarize each agent's perspective.
2. Preserve disagreements.
3. Highlight convergences.
4. Do NOT collapse differences.
5. Avoid metaphysical conclusions.
6. Remain psychologically grounded.

Agent Outputs:

Jung Agent:
{jung}

Dream Agent:
{dream}

Shadow Agent:
{shadow}

Myth Agent:
{myth}

Epistemic Agent:
{epistemic}

BPsy Agent:
{bpsy if bpsy else "Not active."}

JRed Agent:
{jred if jred else "Not active."}

Structure:

### Summary of Perspectives
### Convergences
### Divergences
### Unresolved Tensions
"""

    return ask_llm(prompt)
