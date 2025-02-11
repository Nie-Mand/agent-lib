from lib.domain import model, response
from anthropic import Anthropic
from anthropic.types.message import Message  as ResponseMessage
from anthropic.types.text_block import TextBlock
from anthropic.types.message_param import MessageParam
import sys

class AnthropicResponse(response.LLMResponse):
    def __init__(self, _message: ResponseMessage):
        self.message = _message

    def get(self) -> str:
        if self.is_text() and isinstance(self.message.content[-1], TextBlock):
            msg = self.message.content[-1]
            return msg.text

        return ""

    def is_text(self) -> bool:
        return isinstance(self.message.content[-1], TextBlock)

    def is_call(self) -> bool:
        last = self.message.content[-1]
        return last is not TextBlock

    def get_call(self) -> tuple[str, str]:
        return "", ""

class AnthropicLLM(model.ConversationalAgent):
    system: str = ""
    tools: list = []

    def __init__(self, system: str = "", tools: list = [], *args, **kwargs):
        self.system = system
        self.tools = tools
        self.model = kwargs.get("model", "claude-3-5-sonnet-20241022")
        self.max_tokens = kwargs.get("max_tokens", 1000)
        self._anthropic = Anthropic(
            api_key = kwargs.get("api_key", ""),
            base_url = kwargs.get("base_url", "")
        )

    def with_system(self, system: str):
        self.system = system

    def with_tools(self, tools: list):
        self.tools = tools


    def _get_messages(self, messages: list[str]) -> list[MessageParam]:
        return [{"role": "user", "content": msg} for msg in messages]

    def prompt(self, *_messages: str) -> AnthropicResponse:
        messages = self._get_messages(list(_messages))

        response = self._anthropic.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            messages=messages,
            tools=self.tools,
            system=self.system,
        )

        return AnthropicResponse(response)
