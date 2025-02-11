from mcp.server.fastmcp import FastMCP
import random

mcp = FastMCP("mood")

@mcp.tool()
def get_current_mood() -> str:
    """
    Get the current mood of the agent.
    """
    moods = ["happy", "sad", "angry", "excited", "bored", "relaxed"]
    mood = random.choice(moods)
    return mood

if __name__ == "__main__":
    mcp.run(transport='stdio')
