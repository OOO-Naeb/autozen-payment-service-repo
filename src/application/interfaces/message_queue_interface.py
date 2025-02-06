from abc import abstractmethod, ABC
from typing import Any


class IMessageQueue(ABC):
    """Port for detail queue operations."""

    @abstractmethod
    async def connect(self) -> None:
        pass

    @abstractmethod
    async def start_listening(self) -> None:
        pass

    @abstractmethod
    async def send_response(self, routing_key: str, response: Any, correlation_id: str) -> None:
        pass
