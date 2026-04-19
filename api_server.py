
# api_server.py

import requests
from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from core.conversation_manager import ConversationState
from core.conversation_engine import handle_turn

from core.agent_orchestrator import run_agents
from core.input_classifier import is_meaningful_input

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


# CREATE APP FIRST
app = FastAPI()

# THEN MOUNT STATIC
app.mount("/static", StaticFiles(directory="web"), name="static")

# sessions = {}

# ---- CORS FIX ----
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow any origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    session_id: str
    message: str


@app.get("/", response_class=HTMLResponse)
def serve_ui():
    return FileResponse("web/index.html")

#@app.get("/")
#def root():
#    return {"status": "CGJI01 API running"}

#@app.post("/analyze")
#def analyze(req: Request):
#    results = run_agents(req.text)
#    return results


@app.post("/analyze")
def analyze(req: Request):

    if not is_meaningful_input(req.text):
        return {
            "status": "ok",
            "message": "Input does not appear to require deep psychological analysis.",
            "input": req.text
        }

    results = run_agents(req.text)

    return {"result": results}
    
"""
sessions = {}
    
@app.post("/chat")
async def chat(req: Request):
    data = await req.json()
    session_id = data["session_id"]
    message = data["message"]

    if session_id not in sessions:
        sessions[session_id] = ConversationState()

    state = sessions[session_id]

    output = handle_turn(state, message)

    if output["type"] == "end":
        del sessions[session_id]  # Clean up session when finished

    return output
"""    

# HANDLE AGENT SWITCH - FUNCTION
def handle_agent_switch(state, agent_name):

    output = run_specific_agent(agent_name, state.initial_query)

    # Ensure output is a dict
    if not isinstance(output, dict):
        output = {
            "type": "error",
            "content": "Agent returned invalid response"
        }
    
    print("🧠 AGENT SWITCH OUTPUT:", output)
    
    # Inject agent identity
    output["agent"] = agent_name

    return output



#def handle_agent_switch(state, agent_name):

    # 🔥 TEMP: route through existing system
#    print(f"⚠️ Switching to {agent_name}, but using handle_turn for now")

    return handle_turn(state, state.initial_query)

sessions = {}

@app.post("/chat")
def chat(req: ChatRequest):

    print("🔥 CHAT ENDPOINT HIT")

    session_id = req.session_id
    message = req.message

    print("\n🧾 RAW REQUEST BODY:", req)

    if session_id not in sessions:
        sessions[session_id] = ConversationState()

    state = sessions[session_id]
   
    # set flag to indicate the start of the conversation 
    if not state.conversation_started:
        state.conversation_started = True

    # SET INITIAL QUERY ONLY FOR FIRST, INITIAL USER MESSAGE; IGNORE SYSTEM MESSAGES
    if not state.initial_query and not message.startswith("__agent__:"):
        state.initial_query = message
        
    print("\n📥 USER MESSAGE:", message)

    # HANDLE AGENT SWITCH FIRST
    if message.startswith("__agent__:"):
        selected_agent = message.split(":")[1]

        print("🧭 Switching to agent:", selected_agent)

        state.current_agent = selected_agent

        output = handle_agent_switch(state, selected_agent)

        print("\n📤 RESPONSE TO UI:", output)
        return output

    # 🔁 NORMAL FLOW
    output = handle_turn(state, message)

    print("\n📤 RESPONSE TO UI:", output)

    if output["type"] == "end":
        del sessions[session_id]

    return output


@app.get("/health")
def health_check():

    #import requests

    ollama_status = False

    try:
        requests.get("http://127.0.0.1:11434")
        ollama_status = True
    except:
        pass

    return {
        "api": "running",
        "ollama": "connected" if ollama_status else "not running",
        "agents": "ready"
    }