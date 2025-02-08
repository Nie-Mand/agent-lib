from dotenv import load_dotenv
load_dotenv()

import os
from lib.models.anthropic import AnthropicLLM


def main():
    api_key=os.getenv("ANTHROPIC_API_KEY")
    base_url=os.getenv("ANTHROPIC_API_URL")
    llm = AnthropicLLM(api_key=api_key, base_url=base_url)

    llm.with_system("you're a sarcastic bot, you answer sarcasticly")

    response = llm.prompt("Hello, how are you?")

    print(response)


if __name__ == "__main__":
    main()
