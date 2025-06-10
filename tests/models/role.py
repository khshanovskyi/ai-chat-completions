from task.models.role import Role


class TestRole:
    """Test Role enum"""

    def test_role_values(self):
        assert Role.SYSTEM == "system"
        assert Role.USER == "user"
        assert Role.AI == "assistant"

    def test_role_string_enum(self):
        assert isinstance(Role.SYSTEM, str)
        assert str(Role.USER) == "user"