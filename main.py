from dotenv import load_dotenv
load_dotenv()

import os
from lib.models.azure_ai_inference import AzureAIInferece


def main():
    github_token=os.getenv("GITHUB_TOKEN")
    llm = AzureAIInferece(token=github_token)

    llm.with_system("you're a sarcastic bot, you answer sarcasticly")

    response = llm.prompt("Hello, how are you?")

    print(response)


if __name__ == "__main__":
    main()
