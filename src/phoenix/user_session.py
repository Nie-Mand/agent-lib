import phoenix.domain.metadata as metadata
import uuid

class UserSession(metadata.Metadata):
    def __init__(self):
        self.id = str(uuid.uuid4())

    def get_id(self) -> str:
        return self.id

    def to_string(self) -> str:
        return ""
