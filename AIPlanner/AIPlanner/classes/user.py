# Megdalia Bromhal - 26 Sept. 2024
# User class

#Adding comments for Sprint0 - Archer
class User:
    """A class that represents a user for the system."""
    username: str
    canvas_hash_id: int
    password: str

    def __init__(self, username: str, canvas_hash_id: int, password: str):
        """Initializing user's characteristics."""
        self.username = username
        self.canvas_hash_id = canvas_hash_id
        self.password = password

    def describe_account(self):
        return f"{self.username}'s password is {self.password} and the canvas hash id is {self.canvas_hash_id}!"


EXAMPLE_USER = [User("bobby", '0156372', "bobisawesome"), User("henrythebeast", '0883737372', "yothisishenry")]

for user in EXAMPLE_USER:
    print(User.describe_account(user))