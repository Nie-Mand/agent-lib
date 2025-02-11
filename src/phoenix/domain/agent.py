from abc import ABC, abstractmethod
from src.phoenix.domain.metadata import Metadata

class Agent(ABC):
    @abstractmethod
    async def call(self, _query: str, _metadata: Metadata) -> str:
        pass
