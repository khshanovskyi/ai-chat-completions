from aidial_client import Dial, AsyncDial

from task.clients.base import BaseClient
from task.constants import DIAL_ENDPOINT
from task.models.message import Message
from task.models.role import Role


class DialClient(BaseClient):

    def __init__(self, deployment_name: str):
        super().__init__(deployment_name)
        self._client = Dial(
            base_url=DIAL_ENDPOINT,
            api_key=self._api_key,
        )
        self._async_client = AsyncDial(
            base_url=DIAL_ENDPOINT,
            api_key=self._api_key,
        )

    def get_completion(self, messages: list[Message]) -> Message:
        response = self._client.chat.completions.create(
            deployment_name=self._deployment_name,
            stream=False,
            messages=[msg.to_dict() for msg in messages],
        )

        if choices := response.choices:
            if message := choices[0].message:
                print(message.content)
                return Message(Role.AI, message.content)

        raise Exception("No choices in response found")

    async def stream_completion(self, messages: list[Message]) -> Message:
        chunks = await self._async_client.chat.completions.create(
            deployment_name=self._deployment_name,
            messages=[msg.to_dict() for msg in messages],
            stream=True,
        )

        contents = []
        async for chunk in chunks:
            if chunk.choices and len(chunk.choices) > 0:
                delta = chunk.choices[0].delta
                if delta and delta.content:
                    print(delta.content, end='')
                    contents.append(delta.content)

        print()
        return Message(Role.AI, ''.join(contents))
