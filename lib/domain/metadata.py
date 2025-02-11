from abc import ABC, abstractmethod

class Metadata(ABC):
    @abstractmethod
    def get_id(self) -> str:
        return ""

    @abstractmethod
    def to_string(self) -> str:
        return ""
