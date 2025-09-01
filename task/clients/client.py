from aidial_client import Dial, AsyncDial

from task.clients.base import BaseClient
from task.constants import DIAL_ENDPOINT
from task.models.message import Message
from task.models.role import Role


class DialClient(BaseClient):

    def __init__(self, deployment_name: str):
        super().__init__(deployment_name)
        #TODO:
        # Documentation: https://pypi.org/project/aidial-client/
        # 1. Create Dial client with:
        #   - base_url=DIAL_ENDPOINT
        #   - api_key=self._api_key
        # 2. Create AsyncDial client with:
        #   - base_url=DIAL_ENDPOINT
        #   - api_key=self._api_key

    def get_completion(self, messages: list[Message]) -> Message:
        #TODO:
        # 1. Create chat completions with client (client.chat.completions.create) with such params:
        #   - deployment_name=self._deployment_name
        #   - messages=[msg.to_dict() for msg in messages]
        # 2. Check if 'choices' are present in `response`
        #       -> check if message is present in `choices[0]`
        #           -> print message content and return message with assistant role and message content
        # 3. If choices are not present then raise Exception("No choices in response found")
        raise NotImplementedError

    async def stream_completion(self, messages: list[Message]) -> Message:
        #TODO:
        # 1. Create chat completions with client (async_client.chat.completions.create) with such params:
        #   - deployment_name=self._deployment_name
        #   - messages=[msg.to_dict() for msg in messages]
        #   - stream=True
        # 2. Create array with `contents` name (here we will collect all content chunks)
        # 3. Make async loop from `chunks` (from 1st step)
        # 4. If chunk has choices and their len > 0 then:
        #       -> get it's `delta`
        #           -> if delta is present and has content
        #               -> print(delta.content, end='') and add content to `contents` array
        # 5. Print empty row `print()` (it will represent the end of streaming and in console we will print input from a new line)
        # 6. Return Message with assistant role and message content (`''.join(contents)`)
        raise NotImplementedError
