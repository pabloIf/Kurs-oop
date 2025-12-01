
class User:
    def __init__(self, user_id, username, password, role="user"):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.role = role

    collection = "users"
    id_field = "user_id"

    def to_json(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "password": self.password,
            "role": self.role
        }
    
    def __str__(self):
        return (
            f"\nUser #{self.user_id}\n"
            f"Username: {self.username}\n"
            f"Role: {self.role}\n"
        )