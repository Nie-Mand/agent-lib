from abc import ABC, abstractmethod

class Metadata(ABC):
    @abstractmethod
    def to_string(self) -> str:
        return ""
