class AgentRegistry:

    def __init__(self):
        self.agents = {}

    def register(self, agent):
        self.agents[agent.name] = agent

    def unregister(self, name):
        self.agents.pop(name, None)

    def get(self, name):
        return self.agents.get(name)

    def exists(self, name):
        return name in self.agents

    def list(self):
        return list(self.agents.values())

    def names(self):
        return list(self.agents.keys())