import os

DEFAULT_SYSTEM_PROMPT = "You are an assistant who answers concisely and informatively."
DIAL_ENDPOINT = "https://ai-proxy.lab.epam.com/openai/deployments/{model}/chat/completions"
API_KEY = os.getenv('DIAL_API_KEY', '')