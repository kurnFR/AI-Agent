from abc import ABC, abstractmethod


class BaseTool(ABC):

    name = ""

    @abstractmethod
    def execute(self, plan):
        pass