from phoenix.domain import history
from phoenix.domain.agent import Agent as CoreAgent
from phoenix.domain.metadata import Metadata
from phoenix.domain.history import History
from phoenix.domain.model import ConversationalAgent
from phoenix.domain.tools_connector import ToolsConnector
from phoenix.connectors.dummy import DummyConnector

class Agent(CoreAgent):
    def __init__(self,
        _brain: ConversationalAgent,
        _history: History,
        _connector: ToolsConnector = DummyConnector(),
        _system: str = "",
        _tools: list = []
    ):
        self.brain = _brain
        self.tools = _tools
        self.history = _history
        self.system = _system
        self.connector = _connector

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
