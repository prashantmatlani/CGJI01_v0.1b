

# CONVERSATION MANAGER - core/conversation_manager.py

class ConversationState:
    def __init__(self):
        self.stage = "jung"
        self.history = []
        self.initial_query = None

        self.current_agent = "jung"
        self.agent_histories = {}
        
        self.conversation_started = False # Flag to track the start of the conversation

    # -----------------------------
    # ADD USER INPUT (SINGLE SOURCE)
    # -----------------------------
    def add_user_input(self, text):

        # Prevent duplicate consecutive entries
        if self.history and self.history[-1]["role"] == "client" and self.history[-1]["content"] == text:
            return

        self.history.append({"role": "client", "content": text})

        agent = self.current_agent

        if agent not in self.agent_histories:
            self.agent_histories[agent] = []

        self.agent_histories[agent].append({
            "role": "client",
            "text": text
        })

    # -----------------------------
    # ADD AGENT OUTPUT
    # -----------------------------
    def add_system_output(self, text):

        if self.history and self.history[-1]["role"] == "agent" and self.history[-1]["content"] == text:
            return

        self.history.append({"role": "agent", "content": text})

        agent = self.current_agent

        if agent not in self.agent_histories:
            self.agent_histories[agent] = []

        self.agent_histories[agent].append({
            "role": "agent",
            "text": text
        })