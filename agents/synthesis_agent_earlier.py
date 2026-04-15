

#SYNTHESIS AGENT — agents/synthesis_agent.py - Earlier


from core.llm_client import ask_llm

"""
def synthesize(outputs):
    result = "\n\n=== JI01 MULTI-AGENT SYNTHESIS ===\n"

    for agent, output in outputs.items():
        result += f"\n--- {agent.upper()} AGENT ---\n{output}\n"

    result += "\n=== END SYNTHESIS ==="
    return result
"""

def synthesize(agent_outputs: dict):

    jung = agent_outputs.get("jung", "")
    dream = agent_outputs.get("dream", "")
    shadow = agent_outputs.get("shadow", "")
    myth = agent_outputs.get("myth", "")
    epistemic = agent_outputs.get("epistemic", "")

    prompt = f"""
You are a senior Jungian analyst synthesizing multiple analytical perspectives.

Integrate the following into one coherent professional synthesis.

JUNG ANALYSIS:
{jung}

DREAM ANALYSIS:
{dream}

SHADOW ANALYSIS:
{shadow}

MYTH ANALYSIS:
{myth}

EPISTEMIC ANALYSIS:
{epistemic}

Produce:
- A unified psychological interpretation
- Core dynamic summary
- Clinical implications (if relevant)
- Developmental direction
"""

    return ask_llm(prompt)