from lib.domain import history, metadata

class ChatHistory(history.History):
    def __init__(self):
        self.histories = {}

    def push(self, message_type, message, _metadata: metadata.Metadata):
        if _metadata.get_id() not in self.histories:
            self.histories[_metadata.get_id()] = []

        if message_type == "user" or message_type == "assistant":
            self.histories[_metadata.get_id()].append({
                    "role": message_type,
                    "content": message
            })
        elif message_type == "tool":
            self.histories[_metadata.get_id()].append({
                    "role": "tool",
                    "tool_call_id": message["id"],
                    "content": message["content"],
                    "name": message["name"]
            })
        else:
            self.histories[_metadata.get_id()].append(message)

    def get(self, _metadata: metadata.Metadata) -> list:
        return self.histories[_metadata.get_id()]
