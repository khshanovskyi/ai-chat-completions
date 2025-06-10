import pytest
import json
from unittest.mock import patch

import requests
from aioresponses import aioresponses

from task.models.role import Role
from task.models.message import Message
from task.client import DialClient


class TestDialClient:
    """Test DialClient class"""

    def setup_method(self):
        """Setup test fixtures"""
        self.endpoint = "https://ai-proxy.lab.epam.com/openai/deployments/{model}/chat/completions"
        self.deployment_name = "anthropic.claude-sonnet-4-20250514-v1:0"
        self.api_key = "test-api-key"

    def test_client_creation_valid_params(self):
        """Test DialClient creation with valid parameters"""
        client = DialClient(self.endpoint, self.deployment_name, self.api_key)

        # Test that endpoint is properly formatted
        expected_endpoint = self.endpoint.format(model=self.deployment_name)
        assert client._endpoint == expected_endpoint
        assert client._api_key == self.api_key

    def test_client_creation_empty_api_key(self):
        """Test DialClient creation with empty API key raises ValueError"""
        with pytest.raises(ValueError, match="API key cannot be null or empty"):
            DialClient(self.endpoint, self.deployment_name, "")

    def test_client_creation_none_api_key(self):
        """Test DialClient creation with None API key raises ValueError"""
        with pytest.raises(ValueError, match="API key cannot be null or empty"):
            DialClient(self.endpoint, self.deployment_name, '')

    def test_client_creation_whitespace_api_key(self):
        """Test DialClient creation with whitespace-only API key raises ValueError"""
        with pytest.raises(ValueError, match="API key cannot be null or empty"):
            DialClient(self.endpoint, self.deployment_name, "   ")

    def test_endpoint_formatting(self):
        """Test that endpoint is properly formatted with deployment name"""
        client = DialClient(self.endpoint, "test-model", self.api_key)
        expected = "https://ai-proxy.lab.epam.com/openai/deployments/test-model/chat/completions"
        assert client._endpoint == expected


class TestDialClientSyncCompletion:
    """Test DialClient synchronous completion methods"""

    def setup_method(self):
        """Setup test fixtures"""
        self.endpoint = "https://ai-proxy.lab.epam.com/openai/deployments/{model}/chat/completions"
        self.deployment_name = "test-model"
        self.api_key = "test-api-key"
        self.client = DialClient(self.endpoint, self.deployment_name, self.api_key)
        self.messages = [
            Message(Role.SYSTEM, "You are helpful"),
            Message(Role.USER, "Hello")
        ]

    def test_get_completion_success(self, requests_mock):
        """Test successful get_completion request"""
        # Mock response
        mock_response = {
            "choices": [{
                "message": {
                    "role": "assistant",
                    "content": "Hello! How can I help you today?"
                }
            }]
        }

        expected_url = "https://ai-proxy.lab.epam.com/openai/deployments/test-model/chat/completions"
        requests_mock.post(expected_url, json=mock_response, status_code=200)

        with patch('builtins.print') as mock_print:
            result = self.client.get_completion(self.messages)

        # Verify result
        assert result.role == Role.AI
        assert result.content == "Hello! How can I help you today?"

        # Verify print was called
        mock_print.assert_called_once_with("Hello! How can I help you today?")

        # Verify request was made correctly
        assert requests_mock.call_count == 1
        request = requests_mock.request_history[0]
        assert request.method == "POST"
        assert "api-key" in request.headers
        assert request.headers["api-key"] == self.api_key
        assert request.headers["Content-Type"] == "application/json"

        # Verify request body
        request_data = request.json()
        assert "messages" in request_data
        assert len(request_data["messages"]) == 2
        assert request_data["messages"][0]["role"] == "system"
        assert request_data["messages"][1]["role"] == "user"

    def test_get_completion_no_choices(self, requests_mock):
        """Test get_completion with no choices in response"""
        mock_response = {"choices": []}
        expected_url = "https://ai-proxy.lab.epam.com/openai/deployments/test-model/chat/completions"
        requests_mock.post(expected_url, json=mock_response, status_code=200)

        with pytest.raises(ValueError, match="No Choice has been present in the response"):
            self.client.get_completion(self.messages)

    def test_get_completion_missing_choices(self, requests_mock):
        """Test get_completion with missing choices key"""
        mock_response = {"data": "some other data"}
        expected_url = "https://ai-proxy.lab.epam.com/openai/deployments/test-model/chat/completions"
        requests_mock.post(expected_url, json=mock_response, status_code=200)

        with pytest.raises(ValueError, match="No Choice has been present in the response"):
            self.client.get_completion(self.messages)

    def test_get_completion_http_error(self, requests_mock):
        """Test get_completion with HTTP error response"""
        expected_url = "https://ai-proxy.lab.epam.com/openai/deployments/test-model/chat/completions"
        requests_mock.post(expected_url, text="Bad Request", status_code=400)

        with pytest.raises(Exception, match="HTTP 400: Bad Request"):
            self.client.get_completion(self.messages)

    def test_get_completion_network_error(self, requests_mock):
        """Test get_completion with network error"""
        expected_url = "https://ai-proxy.lab.epam.com/openai/deployments/test-model/chat/completions"
        requests_mock.post(expected_url, exc=requests.exceptions.ConnectTimeout)

        with pytest.raises(Exception):
            self.client.get_completion(self.messages)

    def test_get_completion_with_none_content(self, requests_mock):
        """Test get_completion when API returns None content"""
        mock_response = {
            "choices": [{
                "message": {
                    "role": "assistant",
                    "content": None
                }
            }]
        }

        expected_url = "https://ai-proxy.lab.epam.com/openai/deployments/test-model/chat/completions"
        requests_mock.post(expected_url, json=mock_response, status_code=200)

        with patch('builtins.print') as mock_print:
            result = self.client.get_completion(self.messages)

        # Should handle None content gracefully
        assert result.role == Role.AI
        assert result.content is None
        mock_print.assert_called_once_with(None)

    def test_get_completion_empty_content(self, requests_mock):
        """Test get_completion with empty string content"""
        mock_response = {
            "choices": [{
                "message": {
                    "role": "assistant",
                    "content": ""
                }
            }]
        }

        expected_url = "https://ai-proxy.lab.epam.com/openai/deployments/test-model/chat/completions"
        requests_mock.post(expected_url, json=mock_response, status_code=200)

        with patch('builtins.print') as mock_print:
            result = self.client.get_completion(self.messages)

        assert result.role == Role.AI
        assert result.content == ""
        mock_print.assert_called_once_with("")

    def test_get_completion_malformed_response(self, requests_mock):
        """Test get_completion with malformed response structure"""
        mock_response = {
            "choices": [{
                "message": {
                    "role": "assistant"
                    # Missing "content" key
                }
            }]
        }

        expected_url = "https://ai-proxy.lab.epam.com/openai/deployments/test-model/chat/completions"
        requests_mock.post(expected_url, json=mock_response, status_code=200)

        with patch('builtins.print') as mock_print:
            result = self.client.get_completion(self.messages)

        # Should handle missing content key gracefully
        assert result.role == Role.AI
        assert result.content is None
        mock_print.assert_called_once_with(None)


class TestDialClientAsyncCompletion:
    """Test DialClient asynchronous completion methods"""

    def setup_method(self):
        """Setup test fixtures"""
        self.endpoint = "https://ai-proxy.lab.epam.com/openai/deployments/{model}/chat/completions"
        self.deployment_name = "test-model"
        self.api_key = "test-api-key"
        self.client = DialClient(self.endpoint, self.deployment_name, self.api_key)
        self.messages = [
            Message(Role.SYSTEM, "You are helpful"),
            Message(Role.USER, "Hello")
        ]

    @pytest.mark.asyncio
    async def test_stream_completion_success(self):
        """Test successful stream_completion"""
        # Mock streaming response data
        stream_data = [
            'data: {"choices":[{"delta":{"content":"Hello"}}]}',
            'data: {"choices":[{"delta":{"content":" there"}}]}',
            'data: {"choices":[{"delta":{"content":"!"}}]}',
            'data: [DONE]'
        ]

        expected_url = "https://ai-proxy.lab.epam.com/openai/deployments/test-model/chat/completions"

        with aioresponses() as m:
            # Mock the streaming response
            m.post(expected_url, status=200, body='\n'.join(stream_data).encode())

            with patch('builtins.print') as mock_print:
                result = await self.client.stream_completion(self.messages)

            # Verify result
            assert result.role == Role.AI
            assert result.content == "Hello there!"

            # Verify print calls (should print each token without newline, then final newline)
            expected_calls = [
                (("Hello",), {"end": ""}),
                ((" there",), {"end": ""}),
                (("!",), {"end": ""}),
                ((),)  # Final print() call for newline
            ]
            assert mock_print.call_count == 4

    @pytest.mark.asyncio
    async def test_stream_completion_http_error(self):
        """Test stream_completion with HTTP error"""
        expected_url = "https://ai-proxy.lab.epam.com/openai/deployments/test-model/chat/completions"

        with aioresponses() as m:
            m.post(expected_url, status=400, payload={"error": "Bad request"})

            with patch('builtins.print') as mock_print:
                result = await self.client.stream_completion(self.messages)

            # Should return empty AI message on error
            assert result.role == Role.AI
            assert result.content == ""

    def test_get_content_snippet_valid_data(self):
        """Test __get_content_snippet with valid JSON data"""
        valid_data = json.dumps({
            "choices": [{
                "delta": {
                    "content": "Hello"
                }
            }]
        })

        result = self.client._get_content_snippet(valid_data)
        assert result == "Hello"

    def test_get_content_snippet_no_content(self):
        """Test __get_content_snippet with no content in delta"""
        data_no_content = json.dumps({
            "choices": [{
                "delta": {}
            }]
        })

        result = self.client._get_content_snippet(data_no_content)
        assert result == ""

    def test_get_content_snippet_no_choices(self):
        """Test __get_content_snippet with no choices"""
        data_no_choices = json.dumps({"choices": []})

        result = self.client._get_content_snippet(data_no_choices)
        assert result == ""

    def test_get_content_snippet_invalid_json(self):
        """Test __get_content_snippet with invalid JSON"""
        with pytest.raises(json.JSONDecodeError):
            self.client._get_content_snippet("invalid json")
