# DIAL AI Chat Completion Task

A Python implementation task for building a chat application using DIAL API with both synchronous and streaming completions.

## 🎯 Task Overview

Implement a command-line chat application that communicates with the DIAL AI API. You'll need to complete the missing methods in `client.py` and `app.py` following the provided TODO instructions.

## 🎓 Learning Goals

By completing this task, you will learn:
- Work with `/chat/completions` endpoint to communicate with LLM
- Work with REST requests to LLM
- Handle REST responses from LLM
- Handle stream responses from LLM
- Break down illusions of *magic* and *complication* of working with AI API


## 📋 Requirements

- Python 3.11+
- pip
- API key for DIAL service
- Basic understanding of HTTP requests and async/await

## 🔧 Setup

1. **Setup venv: (also can be configured via IDE)**
   ```bash
   python -m venv .venv
   ``` 
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set your API key:**
    - Ensure that you connected to the EPAM VPN
    - Get the DIAL API key here: https://support.epam.com/ess?id=sc_cat_item&table=sc_cat_item&sys_id=910603f1c3789e907509583bb001310c
    - Get available models from: https://ai-proxy.lab.epam.com/openai/models

4. **Project structure:**
   ```
   task/
   ├── models/
   │   ├── conversation.py   ✅ Complete
   │   ├── message.py        ✅ Complete  
   │   └── role.py           ✅ Complete
   ├── clients/
   │   ├── base.py           ✅ Complete
   │   ├── client.py         🚧 TODO: Implement methods
   │   └── custom_client.py  🚧 TODO: Implement methods
   ├── app.py                🚧 TODO: Implement main logic
   └── constants.py          ✅ Update API key
   ```

## 📝 Your Tasks

### If the task in the main branch is hard for you, then switch to the with-detailed-description branch

### 1. Complete `app.py`
Implement the `start()` function:

- Create DIAL client instance (it will use the aidial-client lib)
- Handle user input and conversation flow
- Choose between streaming and regular completion

### 2. Complete `client.py`
Implement these methods following the TODO comments:

- **`get_completion()`** - Synchronous API request
- **`stream_completion()`** - Asynchronous streaming request

### 3. Complete `custom_client.py`
Implement these methods following the TODO comments:

- **`get_completion()`** - Synchronous API request
- **`stream_completion()`** - Asynchronous streaming request
- **`_get_content_snippet()`** - Parse streaming data chunks

### 4. Run application:
- From IDE runner or terminal:
    ```bash
    python -m task.app
    ```

## 🔍 API Reference

### DIAL Endpoint
```
POST https://ai-proxy.lab.epam.com/openai/deployments/{model}/chat/completions
```

<details> 
<summary>Examples of DIAL API requests</summary>

**Only required fields in request body:**
```json
{
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful assistant."
    },
    {
      "role": "user",
      "content": "What is the capital of France?"
    }
  ]
}
```

Full request:
```
POST https://ai-proxy.lab.epam.com/openai/deployments/{model}/chat/completions
api-key: YOUR_API_KEY
Content-Type: application/json

{
  "model": "gpt-4o",
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful assistant."
    },
    {
      "role": "user",
      "content": "What is the capital of France?"
    }
  ],
  "stream": true
}

```

</details> 

<details> 
<summary>Example of DIAL API regular REST responses</summary>

```json
{
  "id": "chatcmpl-BfT2Bjc6XmMrQnqSXaEzr2J6HaBhl",
  "object": "chat.completion",
  "created": 1749222755,
  "model": "gpt-4o-2024-08-06",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Paris is the capital of France.",
        "refusal": null,
        "annotations": []
      },
      "logprobs": null,
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 21,
    "completion_tokens": 131,
    "total_tokens": 152,
    "prompt_tokens_details": {
      "cached_tokens": 0,
      "audio_tokens": 0
    },
    "completion_tokens_details": {
      "reasoning_tokens": 0,
      "audio_tokens": 0,
      "accepted_prediction_tokens": 0,
      "rejected_prediction_tokens": 0
    }
  },
  "system_fingerprint": "fp_ee1d74bde0"
}
```

</details> 


<details> 
<summary>Examples of DIAL API responses from streaming</summary>

<b>Pay attention that it starts from 'data: ' (it has 6 chars and then content)</b>

```
data: {
    "id": "chatcmpl-BgOcXoaiGfrqHDyu9dcOUMFmWNcgL",
    "object": "chat.completion.chunk",
    "created": 1749444117,
    "model": "gpt-4o-2024-08-06",
    "system_fingerprint": "fp_ee1d74bde0",
    "choices": [
        {
            "index": 0,
            "delta": {
                "role": "assistant",
                "content": "",
                "refusal": null
            },
            "logprobs": null,
            "finish_reason": null
        }
    ]
}
```

```
data: {
    "id": "chatcmpl-BgOcXoaiGfrqHDyu9dcOUMFmWNcgL",
    "object": "chat.completion.chunk",
    "created": 1749444117,
    "model": "gpt-4o-2024-08-06",
    "system_fingerprint": "fp_ee1d74bde0",
    "choices": [
        {
            "index": 0,
            "delta": {
                "content": "The capital"
            },
            "logprobs": null,
            "finish_reason": null
        }
    ]
}
```

```
data: {
    "id": "chatcmpl-BgOcXoaiGfrqHDyu9dcOUMFmWNcgL",
    "object": "chat.completion.chunk",
    "created": 1749444117,
    "model": "gpt-4o-2024-08-06",
    "system_fingerprint": "fp_ee1d74bde0",
    "choices": [
        {
            "index": 0,
            "delta": {
                "content": " of France"
            },
            "logprobs": null,
            "finish_reason": null
        }
    ]
}
```

```
data: {
    "id": "chatcmpl-BgOcXoaiGfrqHDyu9dcOUMFmWNcgL",
    "object": "chat.completion.chunk",
    "created": 1749444117,
    "model": "gpt-4o-2024-08-06",
    "system_fingerprint": "fp_ee1d74bde0",
    "choices": [
        {
            "index": 0,
            "delta": {
                "content": " is Paris."
            },
            "logprobs": null,
            "finish_reason": null
        }
    ]
}
```
```
data: {
    "id": "chatcmpl-BgOcXoaiGfrqHDyu9dcOUMFmWNcgL",
    "object": "chat.completion.chunk",
    "created": 1749444117,
    "model": "gpt-4o-2024-08-06",
    "system_fingerprint": "fp_ee1d74bde0",
    "choices": [
        {
            "index": 0,
            "delta": {},
            "logprobs": null,
            "finish_reason": "stop"
        }
    ],
    "usage": {
        "completion_tokens": 7,
        "prompt_tokens": 14,
        "total_tokens": 21
    }
}
```

When streaming is finished it returns `[DONE]`
```
data: [DONE]
```
</details> 

## 🧪 Testing

### TEST scenarios:
<details> 
<summary>Calculator:</summary>

- Prompt:
  ```
  You are a calculator. Your role is to perform mathematical computations and output the result as a number. Do NOT include any words, explanations, or units in your responses. Only provide the numeric result of the calculation.
  ```
- Scenario:
    ```
  Hi, what can u do?
  ```
  ~ '0'. Or 'Hi, I'm calculator and I can...'
    ```
  3*8
  ```
  ~ 24
    ```
  /2
  ```
  ~ 12
    ```
  -3
  ```
  ~ 9
    ```
  ^2
  ```
  ~ 81
</details> 

<details> 
<summary>Ongoing Technical Troubleshooting:</summary>

- Prompt:
  ```
  You are a Python expert and troubleshooting specialist. Your role is to assist in diagnosing and resolving technical issues related to Python programming. Provide clear, concise, and step-by-step solutions, ensuring the user understands the reasoning behind each step. When applicable, include example code, best practices, or alternative approaches. If the issue involves debugging, highlight the root cause and suggest efficient ways to fix or optimize the code. Always prioritize clarity, accuracy, and actionable advice.
  ```
- Scenario:
  ```
  Hi, what can u do?
  ```
  ~ Hi! I specialize in assisting with Python programming issues. Here's how I can help...
    ```
  I'm getting an error while running my Python script.
  ```
  ~ ... What’s the error message?
    ```
  'ModuleNotFoundError: No module named requests'.
  ```
  ~ This means the 'requests' library isn’t installed. You can install it by running `pip install requests`...
    ```
  I tried that, but now it says 'Permission denied'.
  ```
  ~ It seems you might not have the necessary permissions. Try using `sudo pip install` requests or run the command in a virtual environment.
    ```
  I set up the virtual environment, and now it works. But another error came up: 'ConnectionError'.
  ```
  ~ The 'ConnectionError' suggests an issue with your internet or the URL you’re trying to access...
</details> 

## ✅ Main Criteria for Application Functionality:

1. Streaming in Console:
   > Ensure that the application streams output continuously in the console, reflecting real-time interactions or updates.

2. Conversation History Support:
   > The application should support a history of conversations, allowing LLM to see previous interactions.

### 📊 Expected Behavior

```
Provide System prompt or press 'enter' to continue.
> You are a helpful assistant

Type your question or 'exit' to quit.
> Hello, how are you?
AI: Hello! I'm doing well, thank you for asking. How can I help you today?

> What's the weather like?
AI: I don't have access to real-time weather data, but I'd be happy to help you find weather information...

> exit
Exiting the chat. Goodbye!
```


<details> 
<summary>❓ Troubleshooting</summary>

- In case if it is hard to follow TODO instructions you can check the solution in the `completed` branch.
</details> 

# <img src="dialx-banner.png">