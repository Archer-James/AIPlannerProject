# Megdalia Bromhal - 26 Sept. 2024
# User class

import csv


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
    
    def get_username(self):
        return self.username
    
    def get_password(self):
        return self.password
    
    def get_canvas_hash_id(self):
        return self.canvas_hash_id
    
    def set_username(self, username):
        self.username = username

    def set_password(self, password):
        self.password = password

    def set_canvas_hash_id(self, canvas_hash_id):
        self.canvas_hash_id = canvas_hash_id

    # Want to implement private setters and getters (not sure if access will be an issue then?)

def create_user(username, canvas_hash_id, password):
    new_user = User(username=username, canvas_hash_id=canvas_hash_id, password=password)
    
    success_code = append_user_csv(new_user=new_user)

    return new_user, success_code


def append_user_csv(new_user: User):

    try:
        with open("AIPlanner/data/user_database.csv", mode='a') as f:
            writer = csv.writer(f)
            writer.writerow([new_user.get_username(), new_user.get_canvas_hash_id(), new_user.get_password()])

            return 0
        
    except (FileNotFoundError, PermissionError, IOError, csv.Error, Exception) as e:
        return 1
            
    
def show_database():
    for usr in user_database:
        print(usr)

# Temporary database for testing
user_database: list[str] = []

EXAMPLE_USER = [User("bobby", int('0156372'), "bobisawesome"), User("henrythebeast", int('0883737372'), "yothisishenry")]

def show_example_data():
    for user in EXAMPLE_USER:
        print(User.describe_account(user))

# append_user_csv(create_user('bobby@gmail.com', int('55555'), 'imcoolman'))