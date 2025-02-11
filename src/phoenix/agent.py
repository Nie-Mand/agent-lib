from src.phoenix.domain import history
from src.phoenix.domain.agent import Agent as CoreAgent
from src.phoenix.domain.metadata import Metadata
from src.phoenix.domain.history import History
from src.phoenix.domain.model import ConversationalAgent
from src.phoenix.domain.tools_connector import ToolsConnector

class Agent(CoreAgent):
    def __init__(self,
        brain: ConversationalAgent,
        connector: ToolsConnector,
        history: History,
        system: str = "",
        tools: list = []
    ):
        self.brain = brain
        self.tools = tools
        self.history = history
        self.system = system
        self.connector = connector

        self.brain.with_system(self.system)
        self.brain.with_tools(self.tools)

        if self.connector:
            tools = self.connector.list()
            self.brain.with_tools(tools)

    async def call(self, _query: str, _metadata: Metadata) -> str:
        response = self.brain.prompt(_query, _metadata)
        if response.is_call():
            call = response.get_call()
            result = await self.connector.call(call.name, call.arguments)
            self.history.push("tool", {
                "name": call.name,
                "id": call.id,
                "content": result
            }, _metadata)
            response = self.brain.prompt("", _metadata)
            print("result", result)

        return response.get()
