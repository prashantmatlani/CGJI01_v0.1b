

#CORE AGENT TRIGGERS — core/agent_triggers.py

"""
. Rule-based triggers identify common, easy-to-classify patterns
. A “trigger layer” that scans input for clear rules
. Simple dictionary of keywords - If the input matches a rule, we route to that agent
"""

RULE_TRIGGERS = {
    "dream": ["dream", "night vision", "sleeping image"],
    "shadow": ["shadow", "dark side", "hidden self"],
    "myth": ["myth", "legend", "archetype"],
    "epistemic": ["knowledge", "certainty", "truth"],
    "bpsy": ["Buddhist", "meditation", "mindfulness"],
    "jred": ["philosophy", "comparison", "logic"],
    # Add more as needed
}