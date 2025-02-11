from abc import ABC, abstractmethod

class ToolsConnector(ABC):
    @abstractmethod
    def list(self) -> list:
        pass

    @abstractmethod
    async def call(self, tool: str, args: dict):
        pass
