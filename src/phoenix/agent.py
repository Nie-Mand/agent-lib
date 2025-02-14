from phoenix.domain.agent import Agent as CoreAgent
from phoenix.domain.metadata import Metadata
from phoenix.domain.history import History
from phoenix.domain.model import ConversationalAgent
from phoenix.domain.tools_connector import ToolsConnector
from phoenix.connectors.dummy import DummyConnector

class Agent(CoreAgent):
    def __init__(self,
        brain: ConversationalAgent,
        history: History,
        connector: ToolsConnector = DummyConnector(),
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
        out = ""

        while True:
            response = self.brain.prompt(_query, _metadata)
            print("debug", response)

            if response.is_text():
                out += response.get()

            if not response.is_call():
                break

            if response.is_call():
                call = response.get_call()
                result = await self.connector.call(call.name, call.arguments)
                self.history.push("tool", {
                    "name": call.name,
                    "id": call.id,
                    "content": result
                }, _metadata)
                response = self.brain.prompt("", _metadata)
                out += "\"Figuring things out\""

        return out
