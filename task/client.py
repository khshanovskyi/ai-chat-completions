import json
import aiohttp
import requests

from task.models.message import Message
from task.models.role import Role


class DialClient:
    _endpoint: str
    _api_key: str

    def __init__(self, endpoint: str, deployment_name: str, api_key: str):
        if not api_key or api_key.strip() == "":
            raise ValueError("API key cannot be null or empty")

        self._endpoint = endpoint.format(
            model=deployment_name
        )
        self._api_key = api_key

    def get_completion(self, messages: list[Message]) -> Message:
        """
        Send synchronous request to DIAL API and return AI response.
        """
        headers = {
            "api-key": self._api_key,
            "Content-Type": "application/json"
        }

        request_data = {
            "messages": [msg.to_dict() for msg in messages]
        }

        response = requests.post(url=self._endpoint, headers=headers, json=request_data)


        if response.status_code == 200:
            data = response.json()
            choices = data.get("choices", [])
            if choices:
                content = choices[0].get("message", {}).get("content")
                print(content)
                return Message(Role.AI, content)
            raise ValueError("No Choice has been present in the response")
        else:
            raise Exception(f"HTTP {response.status_code}: {response.text}")

    async def stream_completion(self, messages: list[Message]) -> Message:
        """
        Send asynchronous streaming request to DIAL API and return AI response.
        """
        headers = {
            "api-key": self._api_key,
            "Content-Type": "application/json"
        }
        request_data = {
            "stream": True,
            "messages": [msg.to_dict() for msg in messages]
        }
        contents = []

        async with aiohttp.ClientSession() as session:
            async with session.post(url=self._endpoint, headers=headers, json=request_data) as response:
                if response.status == 200:
                    async for line in response.content:
                        line_str = line.decode('utf-8').strip()
                        if line_str.startswith("data: "):
                            data = line_str[6:].strip()
                            if data != "[DONE]":
                                content_snippet = self._get_content_snippet(data)
                                print(content_snippet, end='')
                                contents.append(content_snippet)
                            else:
                                print()
                else:
                    error_text = await response.text()
                    print(f"{response.status} {error_text}")
                return Message(role=Role.AI, content=''.join(contents))

    def _get_content_snippet(self, data: str) -> str:
        """
        Extract content from streaming data chunk.
        """
        data = json.loads(data)
        if choices := data.get("choices"):
            delta = choices[0].get("delta", {})
            return delta.get("content", '')
        return ''

# IMPLEMENTATION HINTS:
#
# For get_completion():
# - Use requests.post() for synchronous HTTP requests
# - Access JSON data with response.json()
# - Extract nested data safely using .get() method
# - Print AI response to console before returning
#
# For stream_completion():
# - Use aiohttp.ClientSession() for async HTTP requests
# - Stream processing: iterate line by line through response
# - Look for lines starting with "data: "
# - Handle "[DONE]" marker to end streaming
# - Print tokens immediately as they arrive (end='')
# - Join all content snippets at the end
#
# For _get_content_snippet():
# - Parse JSON from streaming data
# - Navigate: data["choices"][0]["delta"]["content"]
# - Use .get() method to avoid KeyError
# - Return empty string if any part is missing
#
# Example API Response Structure:
# Regular completion:
# {
#   "choices": [{
#     "message": {
#       "role": "assistant",
#       "content": "Hello! How can I help you?"
#     }
#   }]
# }
#
# Streaming chunk:
# {
#   "choices": [{
#     "delta": {
#       "content": "Hello"
#     }
#   }]
# }