import reflex as rx
from rxconfig import config
from datetime import date, time, timedelta


class User(rx.Model, table=True):
    username: str
    canvas_hash_id: int
    password: str


class Meta:
    primary_key = "canvas_hash_id"


class Task(rx.Model, table=True):
    recur_frequency: int
    due_date: date
    is_deleted: bool
    task_name: str
    description: str
    task_id: int
    priority_level: int
    assigned_block_date: date
    assigned_block_start_time: time
    assigned_block_duration: timedelta

class UserManagementState(rx.State):
    users: list[User] = []  # To hold the list of users
    message: str = ""        # To display success or error messages

    def fetch_all_users(self):
        with rx.session() as session:
            try:
                # Retrieve all users from the database
                self.users = session.exec(User.select()).all()
                self.message = f"Retrieved {len(self.users)} users."
            except Exception as e:
                self.message = f"Error retrieving users: {e}"
    
    def get_user_data(self):
        return [{"username": user.username, "canvas_hash_id": user.canvas_hash_id} for user in self.users]

        
class AddUser(rx.State):
    username: str
    canvas_hash_id: int
    password: str

    def set_username(self, value: str):
        self.username = value

    def set_canvas_hash_id(self, value: int):
        self.canvas_hash_id = value

    def set_password(self, value: str):
        self.password = value

    def add_user(self, new_user):
        with rx.session() as session:
            session.add(
                User(
                    username=self.username, canvas_hash_id=self.canvas_hash_id, password=self.password
                )
                
            )
            session.commit()


def create_user(username:str, canvas_hash_id:int, password:str):
    """
    Function that creates a User function and calls add_user function with that User object.
    """
    new_user = User(username=username, canvas_hash_id=canvas_hash_id, password=password)
    add_user(new_user=new_user)
    

def add_user(new_user:User):
    """
    Starts a database session and adds the new_user User object into the database.
    """
    with rx.session() as session:
        session.add(new_user)
        session.commit()