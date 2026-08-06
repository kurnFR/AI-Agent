class ToolRegistry:

    def __init__(self):

        self._tools = {}

    def register(self, tool):

        self._tools[tool.name] = tool

    def unregister(self, name):

        self._tools.pop(name, None)

    def get(self, name):

        return self._tools.get(name)

    def exists(self, name):

        return name in self._tools

    def list(self):

        return sorted(self._tools.keys())