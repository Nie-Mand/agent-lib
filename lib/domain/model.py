from abc import ABC, abstractmethod
from lib.domain.response import LLMResponse
from lib.domain.metadata import Metadata

class ConversationalAgent(ABC):
    @abstractmethod
    def with_system(self, system: str):
        pass

    @abstractmethod
    def with_tools(self, tools: list):
        pass

    @abstractmethod
    def prompt(self, _message: str, _metadata: Metadata) -> LLMResponse:
        pass
