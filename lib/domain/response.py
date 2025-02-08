from abc import ABC, abstractmethod

class LLMResponse(ABC):
    @abstractmethod
    def get(self) -> str:
        return ""

    @abstractmethod
    def is_text(self)-> bool:
        return True

    @abstractmethod
    def is_call(self) -> bool:
        return False
