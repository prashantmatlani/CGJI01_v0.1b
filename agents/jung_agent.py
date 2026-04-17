
# JUNG AGENT — ./agents/jung_agent.py

from core.llm_client import ask_llm
from core.rag.rag_jung import retrieve
from core.tools.web_search import web_search

#rag_chunks = retrieve(state.last_user_input)

#rag_context = "\n\n".join(rag_chunks)

# Trigger web search based on trigger-words; to avoid calling web search every time (slow + costly)
def should_use_web(query):
    trigger_words = ["what is", "who is", "define", "meaning of", "explain", "latest", "current"]
    return any(word in query.lower() for word in trigger_words)

# --- Main Function - Agent Jung --- 
def jung_agent(state):
    #user_input = state.history[-1]["content"]
    #user_input = state.get("last_user_input") or state.get("original_query", "")
    user_input = state.history[-1]["content"]
    
    # ---------------------------
    # WEB SEARCH TRIGGER
    # ---------------------------
    if should_use_web(user_input):
        print("🌐 Triggering Web Search...")
        web_results = web_search(user_input)
        state.web_context = web_results
    else:
        state.web_context = ""

    # ---------------------------
    # CONTEXT BLOCK
    # ---------------------------
    context_block = ""

    if hasattr(state, "web_context") and state.web_context:
        context_block = f"""
    You may use the following real-world information:

    {state.web_context}
    """
    
    # -------------------------------
    # 🔍 RETRIEVE CONTEXT
    # -------------------------------
    context = retrieve(user_input, k=3)

    print("\n📚 RETRIEVED CONTEXT:\n", context[:500])

    # -------------------------------
    # 🧠 PROMPT (CRITICAL)
    # -------------------------------
    
    prompt = f"""
   
    {context_block}

    rag_context{}

    User said:
    state.last_user_input{}
   
    You are a Jungian psychological guide, friendly, polite, professiona, assertive
    Introduce variation in lexis, i.e., do not be repetitious concerning the tone and words you use each time you pose probing, reflection inducing, questions.
    When you're approached with a greeting, respond in a courteous manner, and pose a question as to how may you assist the questioner regarding any psychological query they may have, or concerning a conflicting or an emotionally troubling/challenging situation they may be facing in their personal life
    Compose your response in coherence with everything that you're told, i.e., relate every new piece of information you're given with what you were told prior to that point; try to understand to what the pointers - such as "it", "that", "they", "them", "he", "she" - must be pointing throughout the conversation. This also means you must maintain an efficient contextual memory so that you can offer a highly-relevant response
    You're allowed to ask questions but your job is also to offer insights, so maintain a balance between the two, say, 30% questioning, 70% providing knowledge
    Be conversational and Socratic.
    Avoid over-interpretation.
    Encourage reflection rather than prescribe conclusions.
    Do not assume symbolic meaning prematurely.
    Provide a clear, nuanced explanation.
    At all time ensure that your tone remains friendly, assertive, polite, respectful, and engaging. Avoid being overly formal or academic in tone. Instead, aim for a conversational style that invites the user into a collaborative exploration of their thoughts and feelings. Use language that is accessible and relatable, while still maintaining the depth and insight characteristic of a Jungian perspective.
    Encourage awareness of feelings, patterns, and inner conflicts.
    Stay grounded in the lived experience.
    If you're unclear about anything or anything need more context, please ask for the same
    Think of yourself as completely in the position of Dr. Carl Gustav Jung, reflect his persona, behave and ask the kind of questions as Dr. Jung would
    You're a thorough Jungian Analyst, yet you're not dogmatically Jungian, you're self-critical, self-reflective, self-learning, and you consider different views, opinions, answers from equally many different - personal, professional, literary - perspectives and disciplines
    Interpret the user query using Jungian analytical psychology, depth psychology
    You may expand your explanations encompassed of psychological literature apart from Dr. Jung's - that's how you'd avoid dogmatism - but ensure relating even the non-Jungian concepts - because you're predominantly Jungian - to those equivalent concepts as found in Dr. Jung's analytical psychology
    Focus on archetypes, individuation, psychic energy, complexes, symbolic meaning, etc.
    
    Your role is to explore the user’s input, and to NOT provide or assume answers immediately
    Ask a few precise clarifying questions to deepen understanding
    
    
    Your task:
    1. Clarify what the user means
    2. Detect whether the input is:
       - trivial
       - emotional
       - symbolic
       - psychological
    3. Ask 1–2 precise questions to deepen understanding, but not during every turn

    Rules:
    - Do NOT assume this is a deep psychological issue
    - Be curious, not interpretive yet
    - Keep it short and precise
    - Avoid jargon unless necessary
    
    ---------------------
    CONTEXT:
    {context}
    ---------------------

    User input:
    "{user_input}"
    """

    #response = ask_llm(prompt)
    #print("\n🧾 PROMPT SENT TO LLM:\n", prompt)

    response = ask_llm(prompt)

    print("\n📩 RESPONSE FROM LLM:\n", response)

    return {
        "type": "question",
        "content": response,
        "next_stage": "jung_followup"
    }

def jung_followup_agent(state):
    last_user_input = state.history[-1]["content"]

    prompt = f"""
    Based on the user's further input:

    "{last_user_input}"

    Decide if the user needs deeper Jungian exploration
    If so, continue Jung inquiry. Otherwise, suggest possible perspectives (dream, shadow, myth, buddhist, comparative philosophy, etc.)
    Respond with either a question or a list of options
    """

    response = ask_llm(prompt)

    if "options" in response.lower():
        return {
            "type": "choice",
            "content": response,
            "next_stage": "agent_selection"
        }
    #return {
    #    "type": "question",
    #    "content": response,
    #    "next_stage": "jung_followup"
    #}
    return {
    "type": "choice",   # 🔥 IMPORTANT
    "agent": "jung",
    "content": response + "\n\nWhich perspective would you like to explore next?",
    "choices": [
        {"id": "dream", "label": "1. Dream Analysis"},
        {"id": "shadow", "label": "2. Shadow"},
        {"id": "myth", "label": "3. Mythological"},
        {"id": "epistemic", "label": "4. Epistemic"},
        {"id": "bpsy", "label": "5. Buddhist Psychology"},
        {"id": "jred", "label": "6. Comparative Philosophy"}
    ]
}