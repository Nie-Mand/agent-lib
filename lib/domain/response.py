from abc import ABC, abstractmethod

class Call:
    def __init__(self, id: str = "", name: str = "", arguments: dict = {}):
        self.id = id
        self.name = name
        self.arguments = arguments


class LLMResponse(ABC):
    @abstractmethod
    def get(self) -> str:
        return ""

    @abstractmethod
    def get_call(self) -> Call:
        return Call()

    @abstractmethod
    def is_text(self)-> bool:
        return True

    @abstractmethod
    def is_call(self) -> bool:
        return False
