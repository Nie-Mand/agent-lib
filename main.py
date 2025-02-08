from lib.utils import mcp_servers_path_getter
from lib.clients import mcp
from dotenv import load_dotenv
import asyncio
load_dotenv()

import os
from lib import utils

from lib.models.azure_ai_inference import AzureAIInferece
from lib.clients.mcp import MCPClient, MCPServer

async def main():
    # github_token=os.getenv("GITHUB_TOKEN")
    # llm = AzureAIInferece(token=github_token)
    # llm.with_system("you're a sarcastic bot, you answer sarcasticly")
    # response = llm.prompt("Hello, how are you?")
    # print(response)

    server = utils.mcp_servers_path_getter()

    servers = [
        MCPServer(path=server("mood.py"))
    ]

    mcp = MCPClient(servers)

    try:
        await mcp.connect()
        tools = await mcp.list()
        print("\nConnected to server with tools:", [tool.name for tool in tools])
    finally:
        await mcp.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
