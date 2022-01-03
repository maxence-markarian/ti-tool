from uuid import UUID


class Visitor:
    """
    An authenticated user.
    """
    def __init__(self, user_id: UUID, username: str):
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False
        self.user_id = user_id
        self.username = username

    def get_id(self):
        return self.user_id.hex

    def __repr__(self):
        return f"Visitor('{self.user_id}')"
