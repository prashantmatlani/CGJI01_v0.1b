

# CONVERSATION MANAGER - core/conversation_manager.py

class ConversationState:
    def __init__(self):
        self.stage = "jung"  # Initial stage always starts with Jung
        self.history = []
        self.active_agents = []
        self.current_stage = "jung"
        self.flags = {}
        
        self.initial_query = None   # stores first user query
        
        self.current_agent = "jung" # track active agent
        self.agent_histories = {}
        
    """
    def add_user_input(self, text):
        self.history.append({"role": "user", "content": text})

    def add_system_output(self, text):
        self.history.append({"role": "assistant", "content": text})
    """
    
    def add_user_input(self, text):
    self.history.append({"role": "client", "content": text})

    agent = self.current_agent

    if agent not in self.agent_histories:
        self.agent_histories[agent] = []

    self.agent_histories[agent].append({
        "role": "client",
        "text": text
    })


    def add_system_output(self, text):
        self.history.append({"role": "agent", "content": text})

        agent = self.current_agent

        if agent not in self.agent_histories:
            self.agent_histories[agent] = []

        self.agent_histories[agent].append({
            "role": "agent",
            "text": text
        })