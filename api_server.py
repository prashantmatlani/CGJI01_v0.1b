
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
    # call respective agent using original query
    return run_specific_agent(agent_name, state.initial_query)



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

    #output = handle_turn(state, message)
    
    print("\n📥 USER MESSAGE:", message)
    output = handle_turn(state, message)
    print("\n📤 RESPONSE TO UI:", output)
    
    if output["type"] == "end":
        del sessions[session_id]
    
    # HANDLE AGENT SWITCH
    if message.startswith("__agent__:"):
        selected_agent = message.split(":")[1]
    
        state.current_agent = selected_agent
    
        # restart flow for that agent using ORIGINAL query
        output = handle_agent_switch(state, selected_agent)
    
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