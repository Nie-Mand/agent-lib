from abc import ABC, abstractmethod
from typing_extensions import Any

class ToolsConnector(ABC):
    @abstractmethod
    def list(self) -> list:
        pass

    @abstractmethod
    async def call(self, tool: str, args: dict) -> Any:
        pass
