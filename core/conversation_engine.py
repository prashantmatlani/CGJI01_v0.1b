
#CORE CONVERSATION ENGINE — core/conversation_engine.py

from core.agent_selector import rule_based_selection, llm_based_selection

from agents.jung_agent import jung_agent, jung_followup_agent
#from agents.dream_agent import dream_entry, dream_confirm
from agents.dream_agent import dream_agent, dream_confirm, dream_interpret
#from agents.dream_agent import dream_agent
from agents.shadow_agent import shadow_response
from agents.myth_agent import myth_response
from agents.epistemic_agent import epistemic_response
from agents.bpsy_agent import bpsy_response
from agents.jred_agent import jred_response

from core.tools.web_search import web_search
from core.tools.search_trigger import needs_web_search

def handle_turn(state, user_input):
    
    # -----------------------------
    # OPTIONAL WEB SEARCH AUGMENT
    # -----------------------------
    search_results = None

    if needs_web_search(user_input):
        print("🌐 Triggering web search...")
        search_results = web_search(user_input)

        # convert results into text block
        if search_results:
            context = "\n\n".join([
                f"{r['title']}\n{r['content']}"
                for r in search_results
            ])

            # inject into state (temporary context)
            state.web_context = context
        else:
            state.web_context = None
    
    
    # 🔒 FORCE CURRENT AGENT CONTROL
    if not hasattr(state, "current_agent") or state.current_agent is None:
        state.current_agent = "jung"
    
    # -----------------------------
    # END SESSION
    # -----------------------------
    if user_input.strip().lower() == "end session":
        return {
            "type": "end",
            "content": "Session ended. You can start a new conversation anytime.",
            "next_stage": None
        }

    # -----------------------------
    # INITIALIZE STAGE
    # -----------------------------
    if not hasattr(state, "stage") or state.stage is None:
        state.stage = "jung"

    state.add_user_input(user_input)
    
    # store per-agent client message
    if hasattr(state, "current_agent"):
        if state.current_agent not in state.agent_histories:
            state.agent_histories[state.current_agent] = []

        state.agent_histories[state.current_agent].append({
            "role": "client",
            "text": user_input
        })
    

    # Route the flow based on current agent
    stage = state.stage
    agent = state.current_agent
    
    
    print(f"🧠 Current Stage: {stage}")
    
    # -----------------------------
    # JUNG FLOW
    # -----------------------------
    if agent == "jung":
        print("\n🟡 ENTERING JUNG AGENT")
        output = jung_agent(state)

    elif agent == "dream":
        output = dream_agent(state)

    elif agent == "shadow":
        output = shadow_response(user_input)

    elif agent == "myth":
        output = myth_response(user_input)

    elif agent == "epistemic":
        output = epistemic_response(user_input)

    elif agent == "bpsy":
        output = bpsy_response(user_input)

    elif agent == "jred":
        output = jred_response(user_input)

    else:
        output = {
            "type": "error",
            "content": "Unknown agent."
        }
    
    # -----------------------------
    # UPDATE STATE
    # -----------------------------
    state.add_system_output(output["content"])
    state.stage = output.get("next_stage")
    #state.stage = None

    #return output
    
    # -----------------------------
    # STORE PER-AGENT MEMORY
    # -----------------------------
    if not hasattr(state, "agent_histories"):
        state.agent_histories = {}

    if not hasattr(state, "current_agent"):
        state.current_agent = "jung"

    if state.current_agent not in state.agent_histories:
        state.agent_histories[state.current_agent] = []

    state.agent_histories[state.current_agent].append({
        "role": "agent",
        "text": output["content"]
    })

    # -----------------------------
    # FINAL RESPONSE TO UI
    # -----------------------------
    return {
        "type": output["type"],
        "agent": state.current_agent,
        "content": output["content"],
        "next_stage": output.get("next_stage"),
        "agent_log": {
            "agent": state.current_agent,
            "history": state.agent_histories[state.current_agent]
        }
    }
    
    
    # -----------------------------
    # Backend Logging - Print conversation-flow on Terminal
    # -----------------------------
    print("\n📜 UPDATED CONVERSATION HISTORY:")
    for msg in state.history:
        print(f"{msg['role'].upper()}: {msg['content']}")
        #print(msg)
    print("-" * 50)