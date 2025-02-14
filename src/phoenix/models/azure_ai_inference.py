import json
from phoenix.domain import model, response, metadata
from phoenix.models.openai_history import ChatHistory
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import ChatCompletions, SystemMessage
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

    def get_call(self) -> response.Call:
        # Only one tool call is supported
        message = self.get_call_message()
        id = message['tool_calls'][0]['id']
        function = message['tool_calls'][0]['function']
        name = function['name']
        arguments = json.loads(function['arguments'])
        return response.Call(id, name, arguments)

    def get_call_message(self):
        return self.message.choices[-1]['message']

    def is_call(self) -> bool:
        message = self.get_call_message()
        if "tool_calls" in message and len(message['tool_calls']) > 0:
            return True
        return False


class AzureAIInferece(model.ConversationalAgent):
    system: str = ""
    tools: list = []

    def __init__(self, system: str = "", tools: list = [], history = ChatHistory(), *args, **kwargs):
        token = kwargs.get("token", "")
        self.system = system
        self.tools = [{
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema
            }
        } for tool in tools]
        self.client = ChatCompletionsClient(
            endpoint="https://models.github.ai/inference",
            credential=AzureKeyCredential(token),
        )


        self.model = kwargs.get("model", "gpt-4o")
        self.max_tokens = kwargs.get("max_tokens", 4096)
        self.temperature = kwargs.get("temperature", 0.7)
        self.chat_history = history

    def with_system(self, system: str):
        self.system = system

    def with_tools(self, tools: list):
        self.tools = [{
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema
            }
        } for tool in tools]

    def prompt(self, _message: str, _metadata: metadata.Metadata) -> AzureAIResponse:
        if len(_message) != 0:
            self.chat_history.push("user", _message, _metadata)

        messages: list = [SystemMessage(self.system)]
        for message in self.chat_history.get(_metadata):
            messages.append(message)

        tools = self.tools
        if len(tools) == 0:
            tools = None

        response = self.client.complete(
            messages=messages,
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            top_p=1,
            tools=tools,
        )

        response = AzureAIResponse(response)

        if response.is_text():
            content = response.get()
            self.chat_history.push("assistant", content, _metadata)

        if response.is_call():
            call = response.get_call_message()
            self.chat_history.push("tool_call", call, _metadata)

        return response
