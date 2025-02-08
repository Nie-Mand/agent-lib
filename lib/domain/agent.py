from abc import ABC, abstractmethod
from metadata import Metadata

class Agent(ABC):
    @abstractmethod
    def call(self, _query: str, _metadata: Metadata):
        pass
