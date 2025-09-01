from abc import ABC, abstractmethod

from task.constants import API_KEY
from task.models.message import Message


class BaseClient(ABC):

    def __init__(self, deployment_name: str):
        api_key = API_KEY
        if not api_key or api_key.strip() == "":
            raise ValueError("API key cannot be null or empty")
        self._api_key = api_key
        self._deployment_name= deployment_name

    @abstractmethod
    def get_completion(self, messages: list[Message]) -> Message:
        """
        Send synchronous request to DIAL API and return AI response.
        """
        ...

    @abstractmethod
    async def stream_completion(self, messages: list[Message]) -> Message:
        """
        Send asynchronous streaming request to DIAL API and return AI response.
        """
        ...