import asyncio

from task.client import DialClient
from task.constants import DEFAULT_SYSTEM_PROMPT, DIAL_ENDPOINT
from task.models.conversation import Conversation
from task.models.message import Message
from task.models.role import Role


async def start(stream: bool) -> None:
    # 1. Create DialClient
    client = DialClient(
        endpoint=DIAL_ENDPOINT,
        deployment_name='gpt-4o',
        api_key='YOUR_API_KEY',
    )

    # 2. Create conversation
    conversation = Conversation()

    # 3. Get system prompt
    print("Provide System prompt or press 'enter' to continue.")
    prompt = input("> ").strip()
    
    if prompt:
        conversation.add_message(Message(Role.SYSTEM, prompt))
        print("System prompt successfully added to conversation.")
    else:
        conversation.add_message(Message(Role.SYSTEM, DEFAULT_SYSTEM_PROMPT))
        print(f"No System prompt provided. Will be used default System prompt: '{DEFAULT_SYSTEM_PROMPT}'")
    
    print()
    
    # 4. Main chat loop
    print("Type your question or 'exit' to quit.")
    while True:
        user_input = input("> ").strip()
    
        # 5. Check for exit
        if user_input.lower() == "exit":
            print("Exiting the chat. Goodbye!")
            break
    
        # 6. Add user message and get AI response
        conversation.add_message(Message(Role.USER, user_input))

        #7. Call LLM
        print("AI:")
        if stream:
            ai_message = await client.stream_completion(conversation.get_messages())
        else:
            ai_message = client.get_completion(conversation.get_messages())

        # Add assistant message to history
        conversation.add_message(ai_message)

asyncio.run(
    start(True)
)
