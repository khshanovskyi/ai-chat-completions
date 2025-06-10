from task.models.role import Role
from task.models.message import Message


class TestMessage:
    """Test Message dataclass"""

    def test_message_creation(self):
        message = Message(Role.USER, "Hello, world!")
        assert message.role == Role.USER
        assert message.content == "Hello, world!"

    def test_message_to_dict(self):
        message = Message(Role.SYSTEM, "You are helpful")
        expected = {
            "role": "system",
            "content": "You are helpful"
        }
        assert message.to_dict() == expected

    def test_message_to_dict_with_ai_role(self):
        message = Message(Role.AI, "I'm here to help")
        expected = {
            "role": "assistant",
            "content": "I'm here to help"
        }
        assert message.to_dict() == expected

    def test_message_equality(self):
        msg1 = Message(Role.USER, "Test")
        msg2 = Message(Role.USER, "Test")
        msg3 = Message(Role.AI, "Test")

        assert msg1 == msg2
        assert msg1 != msg3