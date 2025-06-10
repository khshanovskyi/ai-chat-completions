import pytest
import json
from unittest.mock import patch
from aioresponses import aioresponses

from task.models.role import Role
from task.models.message import Message
from task.models.conversation import Conversation
from task.client import DialClient
from task import constants


class TestIntegration:
    """Integration tests combining multiple components"""

    def setup_method(self):
        """Setup test fixtures"""
        self.endpoint = constants.DIAL_ENDPOINT
        self.deployment_name = "gpt-4o"
        self.api_key = "test-api-key"

    def test_full_conversation_flow_sync(self, requests_mock):
        """Test a full conversation flow with synchronous completion"""
        # Setup client and conversation
        client = DialClient(self.endpoint, self.deployment_name, self.api_key)
        conversation = Conversation()

        # Add system message
        conversation.add_message(Message(Role.SYSTEM, constants.DEFAULT_SYSTEM_PROMPT))

        # Add user message
        conversation.add_message(Message(Role.USER, "Hello, how are you?"))

        # Mock API response
        mock_response = {
            "choices": [{
                "message": {
                    "role": "assistant",
                    "content": "I'm doing well, thank you for asking!"
                }
            }]
        }

        expected_url = constants.DIAL_ENDPOINT.format(model=self.deployment_name)
        requests_mock.post(expected_url, json=mock_response, status_code=200)

        # Get completion and add to conversation
        with patch('builtins.print'):
            ai_message = client.get_completion(conversation.get_messages())
        conversation.add_message(ai_message)

        # Verify conversation state
        assert len(conversation.get_messages()) == 3
        assert conversation.get_messages()[0].role == Role.SYSTEM
        assert conversation.get_messages()[1].role == Role.USER
        assert conversation.get_messages()[2].role == Role.AI
        assert conversation.get_messages()[2].content == "I'm doing well, thank you for asking!"

    @pytest.mark.asyncio
    async def test_full_conversation_flow_async(self):
        """Test a full conversation flow with asynchronous streaming"""
        # Setup client and conversation
        client = DialClient(self.endpoint, self.deployment_name, self.api_key)
        conversation = Conversation()

        # Add messages
        conversation.add_message(Message(Role.SYSTEM, constants.DEFAULT_SYSTEM_PROMPT))
        conversation.add_message(Message(Role.USER, "Tell me a joke"))

        # Mock streaming response
        stream_data = [
            'data: {"choices":[{"delta":{"content":"Why"}}]}',
            'data: {"choices":[{"delta":{"content":" did"}}]}',
            'data: {"choices":[{"delta":{"content":" the"}}]}',
            'data: {"choices":[{"delta":{"content":" chicken"}}]}',
            'data: {"choices":[{"delta":{"content":" cross"}}]}',
            'data: {"choices":[{"delta":{"content":" the"}}]}',
            'data: {"choices":[{"delta":{"content":" road?"}}]}',
            'data: [DONE]'
        ]

        expected_url = constants.DIAL_ENDPOINT.format(model=self.deployment_name)

        with aioresponses() as m:
            m.post(expected_url, status=200, body='\n'.join(stream_data).encode())

            with patch('builtins.print'):
                ai_message = await client.stream_completion(conversation.get_messages())
            conversation.add_message(ai_message)

        # Verify conversation state
        assert len(conversation.get_messages()) == 3
        assert conversation.get_messages()[2].role == Role.AI
        assert conversation.get_messages()[2].content == "Why did the chicken cross the road?"

    def test_conversation_with_multiple_exchanges_sync(self, requests_mock):
        """Test multiple back-and-forth exchanges in sync mode"""
        client = DialClient(self.endpoint, self.deployment_name, self.api_key)
        conversation = Conversation()

        # Add system message
        conversation.add_message(Message(Role.SYSTEM, constants.DEFAULT_SYSTEM_PROMPT))

        expected_url = constants.DIAL_ENDPOINT.format(model=self.deployment_name)

        # First exchange
        conversation.add_message(Message(Role.USER, "What's 2+2?"))

        mock_response_1 = {
            "choices": [{
                "message": {
                    "role": "assistant",
                    "content": "2+2 equals 4."
                }
            }]
        }
        requests_mock.post(expected_url, json=mock_response_1, status_code=200)

        with patch('builtins.print'):
            ai_message_1 = client.get_completion(conversation.get_messages())
        conversation.add_message(ai_message_1)

        # Second exchange
        conversation.add_message(Message(Role.USER, "What about 3+3?"))

        mock_response_2 = {
            "choices": [{
                "message": {
                    "role": "assistant",
                    "content": "3+3 equals 6."
                }
            }]
        }
        requests_mock.post(expected_url, json=mock_response_2, status_code=200)

        with patch('builtins.print'):
            ai_message_2 = client.get_completion(conversation.get_messages())
        conversation.add_message(ai_message_2)

        # Verify final conversation state
        assert len(conversation.get_messages()) == 5  # system + user1 + ai1 + user2 + ai2
        assert conversation.get_messages()[0].role == Role.SYSTEM
        assert conversation.get_messages()[1].role == Role.USER
        assert conversation.get_messages()[1].content == "What's 2+2?"
        assert conversation.get_messages()[2].role == Role.AI
        assert conversation.get_messages()[2].content == "2+2 equals 4."
        assert conversation.get_messages()[3].role == Role.USER
        assert conversation.get_messages()[3].content == "What about 3+3?"
        assert conversation.get_messages()[4].role == Role.AI
        assert conversation.get_messages()[4].content == "3+3 equals 6."

    def test_error_handling_sync(self, requests_mock):
        """Test error handling in synchronous mode"""
        client = DialClient(self.endpoint, self.deployment_name, self.api_key)
        conversation = Conversation()
        conversation.add_message(Message(Role.USER, "Hello"))

        expected_url = constants.DIAL_ENDPOINT.format(model=self.deployment_name)

        # Mock HTTP 400 error
        requests_mock.post(expected_url, text="Bad Request", status_code=400)

        with pytest.raises(Exception, match="HTTP 400: Bad Request"):
            client.get_completion(conversation.get_messages())

    def test_empty_response_handling_sync(self, requests_mock):
        """Test handling of empty choices in response"""
        client = DialClient(self.endpoint, self.deployment_name, self.api_key)
        conversation = Conversation()
        conversation.add_message(Message(Role.USER, "Hello"))

        expected_url = constants.DIAL_ENDPOINT.format(model=self.deployment_name)

        # Mock response with empty choices
        mock_response = {"choices": []}
        requests_mock.post(expected_url, json=mock_response, status_code=200)

        with pytest.raises(ValueError, match="No Choice has been present in the response"):
            client.get_completion(conversation.get_messages())

    @pytest.mark.asyncio
    async def test_streaming_error_handling(self):
        """Test error handling in streaming mode"""
        client = DialClient(self.endpoint, self.deployment_name, self.api_key)
        conversation = Conversation()
        conversation.add_message(Message(Role.USER, "Hello"))

        expected_url = constants.DIAL_ENDPOINT.format(model=self.deployment_name)

        with aioresponses() as m:
            # Mock HTTP 500 error
            m.post(expected_url, status=500, payload={"error": "Internal server error"})

            with patch('builtins.print'):
                result = await client.stream_completion(conversation.get_messages())

            # Should return empty AI message on error
            assert result.role == Role.AI
            assert result.content == ""

    @pytest.mark.asyncio
    async def test_streaming_malformed_data(self):
        """Test streaming with malformed JSON data - should raise JSONDecodeError"""
        client = DialClient(self.endpoint, self.deployment_name, self.api_key)
        conversation = Conversation()
        conversation.add_message(Message(Role.USER, "Hello"))

        # Mock streaming response with malformed data
        stream_data = [
            'data: {"choices":[{"delta":{"content":"Hello"}}]}',
            'data: invalid json here',  # Malformed JSON - this will cause the error
            'data: {"choices":[{"delta":{"content":" world"}}]}',
            'data: [DONE]'
        ]

        expected_url = constants.DIAL_ENDPOINT.format(model=self.deployment_name)

        with aioresponses() as m:
            m.post(expected_url, status=200, body='\n'.join(stream_data).encode())

            with patch('builtins.print'):
                # The current implementation doesn't handle JSON errors gracefully
                with pytest.raises(json.JSONDecodeError):
                    await client.stream_completion(conversation.get_messages())

    @pytest.mark.asyncio
    async def test_streaming_valid_data_only(self):
        """Test streaming with only valid JSON data"""
        client = DialClient(self.endpoint, self.deployment_name, self.api_key)
        conversation = Conversation()
        conversation.add_message(Message(Role.USER, "Hello"))

        # Mock streaming response with only valid data
        stream_data = [
            'data: {"choices":[{"delta":{"content":"Hello"}}]}',
            'data: {"choices":[{"delta":{"content":" world"}}]}',
            'data: {"choices":[{"delta":{"content":"!"}}]}',
            'data: [DONE]'
        ]

        expected_url = constants.DIAL_ENDPOINT.format(model=self.deployment_name)

        with aioresponses() as m:
            m.post(expected_url, status=200, body='\n'.join(stream_data).encode())

            with patch('builtins.print'):
                result = await client.stream_completion(conversation.get_messages())

        # Should get complete valid content
        assert result.role == Role.AI
        assert result.content == "Hello world!"
