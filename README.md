# Phoenix Agents

A framework for building AI agents with modular connectors and LLM integration.

## Installation

```bash
pip install phoenix-agents
```

## Features

- Modular connector system for agent interactions
- Built-in support for Azure AI and OpenAI
- Chat history management
- Extensible agent architecture
- Session management for multi-user scenarios

## Quick Start


Here's a simple example using Phoenix to create a simple AI agent:

```python
from dotenv import load_dotenv
import asyncio
import os

from phoenix.agent import Agent
from phoenix.user_session import UserSession
from phoenix.models.azure_ai_inference import AzureAIInferece
import phoenix.models.openai_history as openai_history

load_dotenv()

async def main():
    # Initialize chat history
    chat_history = openai_history.ChatHistory()

    # Setup LLM with Azure AI
    llm = AzureAIInferece(
        token=os.getenv("GITHUB_TOKEN"),
        history=chat_history
    )

    # Create agent
    agent = Agent(
        brain=llm,
        history=chat_history,
    )

    # Create user session and interact
    session = UserSession()
    response = await agent.call("Hello, how are you?", session)
    print(response)

if __name__ == "__main__":
    asyncio.run(main())
```

Here's a simple example using Phoenix to create a moody AI agent with MCP connectors:

```python
from dotenv import load_dotenv
import asyncio
import os

from phoenix.agent import Agent
from phoenix.user_session import UserSession
from phoenix.models.azure_ai_inference import AzureAIInferece
import phoenix.models.openai_history as openai_history
from phoenix.connectors.mcp import MCPClient, MCPServer

load_dotenv()

async def main():
    # Initialize chat history
    chat_history = openai_history.ChatHistory()

    # Setup LLM with Azure AI
    llm = AzureAIInferece(
        token=os.getenv("GITHUB_TOKEN"),
        history=chat_history
    )

    # Setup MCP connector with servers
    mcp = MCPClient([
        MCPServer(path="path/to/mood.py")
    ])

    try:
        await mcp.connect()

        # Create agent
        agent = Agent(
            brain=llm,
            history=chat_history,
            connector=mcp,
            system="You are a moody AI, you need to know your current mood to know how to respond.",
        )

        # Create user session and interact
        session = UserSession()
        response = await agent.call("Hello, how are you?", session)
        print(response)

    finally:
        await mcp.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
```

## Configuration

The framework uses environment variables for configuration. Create a `.env` file with:

```
GITHUB_TOKEN=your_token_here
```

## Contributing

Contributions are welcome!

## License
MIT

## Documentation
TODO
