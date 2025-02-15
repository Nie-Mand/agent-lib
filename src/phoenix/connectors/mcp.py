from typing_extensions import Any
from phoenix.domain import tools_connector
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class MCPServer:
    # TODO: Support multiple languages
    def __init__(self, path: str):
        self.path = path
        self.command = "python3"


class MCPClient(tools_connector.ToolsConnector):
    def __init__(self, servers: list[MCPServer]):
        self.session: ClientSession
        self.exit_stack = AsyncExitStack()
        self.servers = servers
        self.tools = []

    async def connect(self):
        # TODO: Connect to multiple servers
        server = self.servers[0]

        server_params = StdioServerParameters(
            command=server.command,
            args=[server.path],
            env=None
        )

        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(
                self.stdio, self.write
            )
        )
        await self.session.initialize()

        self.tools = await self._list()

    def list(self) -> list:
        return self.tools

    async def _list(self):
        response = await self.session.list_tools()
        return response.tools

    async def call(self, tool: str, args: dict) -> Any:
        result = await self.session.call_tool(tool, args)
        return [response.text for response in result.content if response.type == "text"]

    async def cleanup(self):
        await self.exit_stack.aclose()
