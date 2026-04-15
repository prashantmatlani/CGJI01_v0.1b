
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

def handle_turn(state, user_input):
    
    
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

    stage = state.stage

    print(f"🧠 Current Stage: {stage}")

    # -----------------------------
    # JUNG FLOW
    # -----------------------------
    if stage == "jung":
        #output = jung_agent(state)
        print("\n🟡 ENTERING JUNG AGENT")
        output = jung_agent(state)
        print("🟢 JUNG AGENT OUTPUT:", output)
        
        
    elif stage == "jung_followup":
        output = jung_followup_agent(state)

    # -----------------------------
    # DREAM FLOW
    # -----------------------------
    elif stage == "dream":
        output = dream_agent(state)

    elif stage == "dream_confirm":
        output = dream_confirm(state)

    elif stage == "dream_interpret":
        output = dream_interpret(state)

    # -----------------------------
    # OTHER AGENTS (fallback mode)
    # -----------------------------
    else:
        selected_agent = rule_based_selection(user_input)

        if not selected_agent:
            selected_agent = llm_based_selection(user_input)

        print(f"🔀 Selected Agent: {selected_agent}")

        if selected_agent == "shadow":
            result = shadow_response(user_input)
        elif selected_agent == "myth":
            result = myth_response(user_input)
        elif selected_agent == "epistemic":
            result = epistemic_response(user_input)
        elif selected_agent == "bpsy":
            result = bpsy_response(user_input)
        elif selected_agent == "jred":
            result = jred_response(user_input)
        else:
            result = "I'm not sure which perspective applies. Could you clarify?"

        output = {
            "type": "response",
            "agent": "jung",   # include agent identity in every response
            "content": result,
            "next_stage": "jung_followup"
        }

    # -----------------------------
    # UPDATE STATE
    # -----------------------------
    state.add_system_output(output["content"])
    state.stage = output.get("next_stage")

    return output
    
    # -----------------------------
    # Backend Logging - Print conversation-flow on Terminal
    # -----------------------------
    print("\n📜 UPDATED CONVERSATION HISTORY:")
    for msg in state.history:
        print(f"{msg['role'].upper()}: {msg['content']}")
        #print(msg)
    print("-" * 50)