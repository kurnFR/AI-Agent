from abc import ABC
from abc import abstractmethod


class BasePlanner(ABC):

    @abstractmethod
    def build_prompt(self, message: str) -> str:
        pass

    @abstractmethod
    def parse_response(self, response: str):
        pass

    @abstractmethod
    def create_plan(self, message: str):
        pass
