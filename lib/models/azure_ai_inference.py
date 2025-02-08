from lib.domain import model, response
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, ChatCompletions, UserMessage
from azure.core.credentials import AzureKeyCredential

class AzureAIResponse(response.LLMResponse):
    def __init__(self, _message: ChatCompletions):
        self.message = _message

    def _get_message(self):
        return self.message.choices[-1].message

    def get(self) -> str:
        return self._get_message().content

    def is_text(self) -> bool:
        msg = self._get_message()
        return msg.content is not None and len(msg.content) > 0


    def is_call(self) -> bool:
        return False


class AzureAIInferece(model.ConversationalAgent):
    system: str = ""
    tools: list = []

    def __init__(self, system: str = "", tools: list = [], *args, **kwargs):
        token = kwargs.get("token", "")
        self.system = system
        self.tools = tools
        self.client = ChatCompletionsClient(
            endpoint="https://models.github.ai/inference",
            credential=AzureKeyCredential(token),
        )


        self.model = kwargs.get("model", "gpt-4o")
        self.max_tokens = kwargs.get("max_tokens", 4096)

    def with_system(self, system: str):
        self.system = system

    def with_tools(self, tools: list):
        self.tools = tools


    def prompt(self, *_messages: str) -> str:
        response = self.client.complete(
            messages=[
                SystemMessage(content=self.system),
                UserMessage(content=_messages[0]),
            ],
            model=self.model,
            temperature=1,
            max_tokens=self.max_tokens,
            top_p=1
        )

        response = AzureAIResponse(response)
        if response.is_text():
            return response.get()

        return ""
