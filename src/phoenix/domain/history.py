from abc import ABC, abstractmethod
from phoenix.domain.metadata import Metadata

class History(ABC):
    @abstractmethod
    def push(self, message_type, message, _metadata: Metadata):
        pass

    @abstractmethod
    def get(self, _metadata: Metadata) -> list:
        pass
