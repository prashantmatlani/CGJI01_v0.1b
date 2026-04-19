
# CGJI01 — Multi-Agent Jungian Intelligence System

CGJI01 is an interactive multi-agent psychological reasoning system designed to simulate deep, multi-perspective inquiry rooted in analytical psychology and related disciplines.

At its core, the system begins with a Jungian analytical framework and expands into a network of specialized agents (Dream, Shadow, Myth, Epistemic, Buddhist Psychology, etc.), enabling layered interpretation and synthesis of human inquiry.

---

## 🧠 SYSTEM OVERVIEW

### Flow of Interaction

1. User initiates conversation ("Fire")
2. Input is routed to **Agent Jung (default entry point)**
3. Jung Agent:
   - Interprets query
   - Retrieves internal knowledge (RAG)
   - Optionally performs web search
   - Produces structured response
4. System continues in **Jung follow-up loop**
5. User may:
   - Continue dialogue (Fuel)
   - Select another agent (via dynamic choice system — upcoming)
6. Selected agent takes control (agent switching)
7. Multi-agent perspectives accumulate
8. Final synthesis (planned via Synthesizer Agent)

---

## 🧩 ARCHITECTURE

### Backend (FastAPI)

api_server.py
↓
conversation_engine.py
↓
agent (jung_agent.py)
↓
LLM (Groq / LLaMA 3.1)

---

### Core Components

#### 1. Conversation State (`conversation_manager.py`)

Maintains:

- Global history
- Per-agent histories
- Current active agent
- Stage tracking
- Initial query (anchor for agent switching)

```python
state = {
    history: [],
    agent_histories: {},
    current_agent: "jung",
    initial_query: "...",
    stage: "jung"
}

2. Conversation Engine (conversation_engine.py)

Central router controlling flow.

Responsibilities:

Handles session lifecycle
Injects web-search context
Locks active agent
Routes to correct agent
Stores memory
Returns structured response to UI

3. Agent Layer

Each agent is modular:

agents/
    jung_agent.py
    dream_agent.py
    shadow_agent.py
    ...

🧠 AGENT JUNG — CORE DESIGN

Agent Jung is the primary intelligence layer and philosophical anchor of the system.

🎯 Objective

To simulate a Jungian analytical psychologist that:

Interprets user input symbolically
Encourages introspection
Guides toward individuation
Avoids shallow informational responses
Maintains psychological depth
⚙️ Functional Pipeline
1. Input Extraction
user_input = state.history[-1]["content"]
2. Web Search (Conditional)

Triggered via heuristic:

should_use_web(query)

Adds:

state.web_context
3. RAG (Retrieval-Augmented Generation)

From:

/rag/jung/jung.index
/rag/jung/jung_texts.txt

Using:

FAISS
sentence-transformers (MiniLM)
retrieve(query, k=3)
4. Context Constructio# CGJI01 — Multi-Agent Jungian Intelligence System

CGJI01 is an interactive multi-agent psychological reasoning system designed to simulate deep, multi-perspective inquiry rooted in analytical psychology and related disciplines.

At its core, the system begins with a Jungian analytical framework and expands into a network of specialized agents (Dream, Shadow, Myth, Epistemic, Buddhist Psychology, etc.), enabling layered interpretation and synthesis of human inquiry.

---

## 🧠 SYSTEM OVERVIEW

### Flow of Interaction

1. User initiates conversation ("Fire")
2. Input is routed to **Agent Jung (default entry point)**
3. Jung Agent:
   - Interprets query
   - Retrieves internal knowledge (RAG)
   - Optionally performs web search
   - Produces structured response
4. System continues in **Jung follow-up loop**
5. User may:
   - Continue dialogue (Fuel)
   - Select another agent (via dynamic choice system — upcoming)
6. Selected agent takes control (agent switching)
7. Multi-agent perspectives accumulate
8. Final synthesis (planned via Synthesizer Agent)

---

## 🧩 ARCHITECTURE

### Backend (FastAPI)

api_server.py
↓
conversation_engine.py
↓
agent (jung_agent.py)
↓
LLM (Groq / LLaMA 3.1)

---

### Core Components

#### 1. Conversation State (`conversation_manager.py`)

Maintains:

- Global history
- Per-agent histories
- Current active agent
- Stage tracking
- Initial query (anchor for agent switching)

```python
state = {
    history: [],
    agent_histories: {},
    current_agent: "jung",
    initial_query: "...",
    stage: "jung"
}
2. Conversation Engine (conversation_engine.py)

Central router controlling flow.

Responsibilities:

Handles session lifecycle
Injects web-search context
Locks active agent
Routes to correct agent
Stores memory
Returns structured response to UI
3. Agent Layer

Each agent is modular:

agents/
    jung_agent.py
    dream_agent.py
    shadow_agent.py
    ...

🧠 AGENT JUNG — CORE DESIGN

Agent Jung is the primary intelligence layer and philosophical anchor of the system.

🎯 Objective

To simulate a Jungian analytical psychologist that:

Interprets user input symbolically
Encourages introspection
Guides toward individuation
Avoids shallow informational responses
Maintains psychological depth
⚙️ Functional Pipeline
1. Input Extraction
user_input = state.history[-1]["content"]
2. Web Search (Conditional)

Triggered via heuristic:

should_use_web(query)

Adds:

state.web_context
3. RAG (Retrieval-Augmented Generation)

From:

/rag/jung/jung.index
/rag/jung/jung_texts.txt

Using:

FAISS
sentence-transformers (MiniLM)
retrieve(query, k=3)

Via:

context_builder.py

Combines:

Jungian knowledge (RAG)
Real-world context (web search)

5. LLM Prompt Injection

Final prompt includes:

User query
Retrieved Jungian concepts
Optional real-world knowledge
Instructional tone constraints

6. Output Format
{
  "type": "question",
  "agent": "jung",
  "content": "...",
  "next_stage": "jung_followup"
}

🧠 Behavioral Characteristics

Agent Jung is designed to:

Ask reflective questions
Avoid premature conclusions
Link ideas to Jungian constructs:
Persona
Shadow
Anima/Animus
Individuation
Self
Integrate cross-disciplinary references:
Buddhism
Mythology
Philosophy

⚠️ Known Issues (Current)

Overuse of greeting phrases
Occasional verbosity
Weak grounding when RAG is sparse
Redundant memory entries (fixed in latest patch)
Web search not yet deeply integrated into reasoning

🌐 WEB SEARCH TOOL

Located at:

./core/tools/web_search.py
Uses Tavily API
Triggered conditionally
Injected into prompt as auxiliary context
Logs usage in backend

📚 RAG SYSTEM

Structure
kb/jung/ → raw text files
rag/jung/
    jung.index
    jung_texts.txt
Build Process
python build_index.py

💻 FRONTEND (Vanilla JS)

Interaction Model
Fire → starts conversation
Fuel → continues conversation
Dynamic agent responses
Per-agent memory panels
UI Components
Chat window
Input box (dynamic placeholder)
Agent panels (Jung, Dream, etc.)
Choice buttons (planned)
End session control

🔁 AGENT MEMORY SYSTEM

Maintains:

window.agentMemory = {
  jung: [...],
  dream: [...]
}

Synced from backend:

agent_log: {
  agent: "jung",
  history: [...]
}

🔮 FUTURE ROADMAP

Immediate
Remove repetitive greetings (prompt refinement)
Stabilize RAG grounding
Clean agent switching UX

Mid-Term
Multi-agent orchestration
Synthesizer agent
Better tool-use reasoning

Advanced
Fine-tuning (LoRA) on Jungian corpus
Personality stabilization
Long-term memory

🧪 DEVELOPMENT NOTES

Built for iterative experimentation
Modular agent design allows scaling
RAG per-agent enables specialization
Web + RAG hybrid = hybrid cognition model

🧭 PHILOSOPHY

CGJI01 is an attempt to model:

"Dialogue as a path to psychological transformation"

Inspired by:

Jungian analytical psychology
Symbolic reasoning
Multi-perspective cognition

⚙️ SETUP
pip install -r requirements.txt

Run:

uvicorn api_server:app --reload
