from abc import ABC, abstractmethod

class ConversationalAgent(ABC):
    @abstractmethod
    def with_system(self, system: str):
        pass

    @abstractmethod
    def with_tools(self, tools: list):
        pass

    @abstractmethod
    def prompt(self, *messages: str) -> str:
        return ""
