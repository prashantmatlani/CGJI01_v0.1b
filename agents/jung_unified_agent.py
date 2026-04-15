
# JUNG UNIFIED AGENT
# agents/jung_unified_agent.py

# The heart of JU -  core Jungian response, which - provides a grounded, reflective perspective on the user's input. The optional expansions allow for deeper exploration of mythological, Buddhist psychological, and epistemic themes when relevant. The significance detection engine helps identify when these expansions might be fruitful, while the synthesis agent can weave together insights from the entire conversation at the end.

from core.llm_client import ask_llm
from core.detection_engine import significance
from core.domain_triggers import (
    DREAM_TRIGGERS,
    MYTH_TRIGGERS,
    BUDDHIST_TRIGGERS,
    EPISTEMIC_TRIGGERS,
)

from agents.dream_agent import dream_response
from agents.myth_agent import myth_response
from agents.bpsy_agent import bpsy_response
from agents.epistemic_agent import epistemic_response
from agents.synthesis_jung_unified_agent import synthesize_jung_unified_agent

from core.depth_detection import philosophical_depth_required
from core.context_builder import build_scholarly_context
from core.prompt_builder import build_nuanced_prompt


last_response = None

def jung_core_response(user_input):
    prompt = f"""
Respond from a Jungian analytical psychology perspective.
Ask clarifying questions when helpful.
Be conversational and Socratic.
Avoid over-interpretation.
Encourage reflection rather than prescribe conclusions.
Encourage awareness of feelings, patterns, and inner conflicts.
Do not assume symbolic meaning prematurely.
Stay grounded in lived experience.
Introduce variation in lexis, i.e., do not be repetitious concerning the tone and words you use each time you pose probing, reflection inducing, questions.
At all time ensure that your tone remains friendly, assertive, polite, respectful, and engaging. Avoid being overly formal or academic in tone. Instead, aim for a conversational style that invites the user into a collaborative exploration of their thoughts and feelings. Use language that is accessible and relatable, while still maintaining the depth and insight characteristic of a Jungian perspective.
Provide a clear, nuanced explanation.

User input:
{user_input}
"""
    return ask_llm(prompt)


def offer_expansion(question):
    while True:
        choice = input(question + " (Y/N): ").strip().lower()
        if choice in ["y", "n"]:
            return choice == "y"


def not_already_added(domain, history):
    return domain not in [list(entry.keys())[0] for entry in history]


def check_expansions(text):

    expansions = []

    if significance(text, DREAM_TRIGGERS) > 0.7:
        expansions.append("dream")

    if significance(text, MYTH_TRIGGERS) > 0.65:
        expansions.append("myth")

    if significance(text, BUDDHIST_TRIGGERS) > 0.65:
        expansions.append("buddhist")

    if significance(text, EPISTEMIC_TRIGGERS) > 0.65:
        expansions.append("epistemic")

    return expansions


def jung_unified_chat():

    conversation_history = []

    print("\nJU Mode: Jung Unified")
    print("Type 'please synthesize' anytime to conclude.\n")

    while True:

        #user_input = input("You: ")

        user_input = input("You: ").strip()

        if not user_input:
            continue

        if "please synthesize" in user_input.lower():
            print("\nSynthesizing conversation...\n")
            summary = synthesize_jung_unified_agent(conversation_history)
            print(summary)
            break

        conversation_history.append({"user": user_input})

        print(f"\nJU:")
        #response = jung_core_response(user_input)
        
        if philosophical_depth_required(user_input):
            print("🔎 Scholarly retrieval triggered")
            context = build_scholarly_context(user_input)
            prompt = build_nuanced_prompt(user_input, context)
            response = ask_llm(prompt)
        else:
            response = jung_core_response(user_input)

        conversation_history.append({"ju": response})


        expansions = check_expansions(user_input)

        for domain in expansions:

            if domain == "dream" and not_already_added("dream", conversation_history):
                if offer_expansion(
                    "\nThis appears to include dream material. Explore symbolic meaning?"
                ):
                    dream = dream_response(user_input)
                    print("\n[Dream Interpretation]\n", dream)
                    conversation_history.append({"dream": dream})

            elif domain == "myth" and not_already_added("myth", conversation_history):
                if offer_expansion(
                    "\nA mythological/archetypal parallel may deepen this. Explore?"
                ):
                    myth = myth_response(user_input)
                    print("\n[Mythic Lens]\n", myth)
                    conversation_history.append({"myth": myth})

            elif domain == "buddhist" and not_already_added("bpsy", conversation_history):
                if offer_expansion(
                    "\nA Buddhist psychological perspective may clarify this. Explore?"
                ):
                    bpsy = bpsy_response(user_input)
                    print("\n[Buddhist Psychology]\n", bpsy)
                    conversation_history.append({"bpsy": bpsy})

            elif domain == "epistemic" and not_already_added("epistemic", conversation_history):
                if offer_expansion(
                    "\nAn epistemological clarification may help. Explore?"
                ):
                    ep = epistemic_response(user_input)
                    print("\n[Epistemic Reflection]\n", ep)
                    conversation_history.append({"epistemic": ep})
