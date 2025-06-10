import uuid

from task.models.role import Role
from task.models.message import Message
from task.models.conversation import Conversation


class TestConversation:
    """Test Conversation dataclass"""

    def test_conversation_creation(self):
        conv = Conversation()
        assert conv.id is not None
        assert len(conv.messages) == 0
        # Test that ID is a valid UUID string
        uuid.UUID(conv.id)  # This will raise if invalid

    def test_conversation_unique_ids(self):
        conv1 = Conversation()
        conv2 = Conversation()
        assert conv1.id != conv2.id

    def test_add_message(self):
        conv = Conversation()
        message = Message(Role.USER, "Hello")

        conv.add_message(message)
        assert len(conv.messages) == 1
        assert conv.messages[0] == message

    def test_add_multiple_messages(self):
        conv = Conversation()
        msg1 = Message(Role.SYSTEM, "System prompt")
        msg2 = Message(Role.USER, "User message")
        msg3 = Message(Role.AI, "AI response")

        conv.add_message(msg1)
        conv.add_message(msg2)
        conv.add_message(msg3)

        assert len(conv.messages) == 3
        assert conv.messages[0] == msg1
        assert conv.messages[1] == msg2
        assert conv.messages[2] == msg3

    def test_get_messages(self):
        conv = Conversation()
        msg1 = Message(Role.USER, "Hello")
        msg2 = Message(Role.AI, "Hi there")

        conv.add_message(msg1)
        conv.add_message(msg2)

        messages = conv.get_messages()
        assert len(messages) == 2
        assert messages[0] == msg1
        assert messages[1] == msg2

        # Test that returned list is the same object (not a copy)
        assert messages is conv.messages
