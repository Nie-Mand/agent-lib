from abc import ABC, abstractmethod

class ToolsConnector(ABC):
    @abstractmethod
    async def list(self) -> list:
        return []

    @abstractmethod
    async def call(self, tool):
        return None
