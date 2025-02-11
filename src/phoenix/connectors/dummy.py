from phoenix.domain import tools_connector

class DummyConnector(tools_connector.ToolsConnector):
    def list(self) -> list:
        return []

    async def call(self, tool: str, args: dict):
        return None
