from lib.utils import mcp_servers_path_getter
from lib.clients import mcp
from dotenv import load_dotenv
import asyncio
load_dotenv()

import os
from lib import utils

from lib.models.azure_ai_inference import AzureAIInferece
import lib.models.openai_history as openai_history
from lib.clients.mcp import MCPClient, MCPServer
from lib.agent import Agent
from lib.user_session import UserSession

async def main():
    # LLM
    chat_history = openai_history.ChatHistory()
    github_token=os.getenv("GITHUB_TOKEN")
    llm = AzureAIInferece(token=github_token, history=chat_history)


    # mcp client
    server = utils.mcp_servers_path_getter()
    servers = [
        MCPServer(path=server("mood.py"))
    ]
    mcp = MCPClient(servers)

    try:
        await mcp.connect()

        agent = Agent(
            brain=llm,
            history=chat_history,
            connector=mcp,
            system="You are a moody AI, you need to know your current mood to know how to respond.",
        )
        session = UserSession()
        response = await agent.call("Hello, how are you?", session)
        print(response)

    finally:
        await mcp.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
