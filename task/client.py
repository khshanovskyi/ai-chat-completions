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
        # TODO:
        # 1. Create headers dictionary with:
        #    - "api-key": self._api_key
        #    - "Content-Type": "application/json"
        # 2. Create request_data dictionary with:
        #    - "messages": convert messages list to dict format using msg.to_dict() for each message
        # 3. Make POST request using requests.post() with:
        #    - URL: self._endpoint
        #    - headers: headers from step 1
        #    - json: request_data from step 2
        # 4. Check if response.status_code == 200:
        #    - If yes: parse JSON response using response.json()
        #    - Get "choices" from response data
        #    - If choices exist and not empty:
        #      * Extract content from choices[0]["message"]["content"]
        #      * Print the content to console
        #      * Return Message(role=Role.AI, content=content)
        #    - If no choices: raise ValueError("No Choice has been present in the response")
        # 5. If status code != 200:
        #    - Raise Exception with format: f"HTTP {response.status_code}: {response.text}"
        pass

    async def stream_completion(self, messages: list[Message]) -> Message:
        """
        Send asynchronous streaming request to DIAL API and return AI response.
        """
        # TODO:
        # 1. Create headers dictionary with:
        #    - "api-key": self._api_key
        #    - "Content-Type": "application/json"
        # 2. Create request_data dictionary with:
        #    - "stream": True  (enable streaming)
        #    - "messages": convert messages list to dict format using msg.to_dict() for each message
        # 3. Create empty list called 'contents' to store content snippets
        # 4. Create aiohttp.ClientSession() using 'async with' context manager
        # 5. Inside session, make POST request using session.post() with:
        #    - URL: self._endpoint
        #    - json: request_data from step 2
        #    - headers: headers from step 1
        #    - Use 'async with' context manager for response
        # 6. Check if response.status == 200:
        #    - If yes: iterate through response.content using 'async for line in response.content:'
        #      * Decode line: line_str = line.decode('utf-8').strip()
        #      * Check if line starts with "data: ":
        #        - Extract data: data = line_str[6:].strip()
        #        - If data != "[DONE]":
        #          + Call self._get_content_snippet(data) to extract content
        #          + Print content snippet without newline: print(content_snippet, end='')
        #          + Append content snippet to contents list
        #        - If data == "[DONE]":
        #          + Print empty line: print()
        #    - If status != 200:
        #      * Get error text: error_text = await response.text()
        #      * Print error: print(f"{response.status} {error_text}")
        # 7. Return Message(role=Role.AI, content=''.join(contents))
        pass

    def _get_content_snippet(self, data: str) -> str:
        """
        Extract content from streaming data chunk.
        """
        # TODO:
        # 1. Parse JSON data using json.loads(data)
        # 2. Get "choices" from parsed JSON data
        # 3. If choices exist and not empty:
        #    - Get delta from choices[0]["delta"]
        #    - Return content from delta.get("content", '') - use empty string as default
        # 4. If no choices, return empty string
        pass


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