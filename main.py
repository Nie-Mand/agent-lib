from dotenv import load_dotenv
import asyncio
load_dotenv()

import os
import utils

from src.phoenix.models.azure_ai_inference import AzureAIInferece
import src.phoenix.models.openai_history as openai_history
from src.phoenix.connectors.mcp import MCPClient, MCPServer
from src.phoenix.agent import Agent
from src.phoenix.user_session import UserSession

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
