class GHUser:
    """Class representing state of a GitHub user"""

    def __init__(self):
        self.id = 0
        self.login = ""
        self.permissions = []

    def print_info(self):
        """Print user info in console"""
        for name, value in vars(self).items():
            print(f"{name} = {value}")

    def to_json(self) -> dict:
        """Convert class to JSON"""
        return {
            "id": self.id,
            "login": self.login,
            "permissions": self.permissions
        }
