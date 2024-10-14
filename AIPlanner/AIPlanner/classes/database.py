"""Module containing classes and methods pertaining to the SQLite database built into Reflex"""
from datetime import date, time, timedelta
import reflex as rx
from rxconfig import config

class User(rx.Model, table=True):
    """Class that defines the User table in the SQLite database
    
    Attributes:
        username: A unique string identifier, allows users 
                  to sign in without a canvas_hash_id specified
        canvas_hash_id: A unique integer identifier, allows tasks to be imported from Canvas
        password: A string used to authenticate user login
    """
    username: str
    canvas_hash_id: int
    password: str

    class Meta:
        """Metadata for User class"""
        primary_key = "canvas_hash_id"

class Task(rx.Model, table=True):
    """Class that defines the Task table in the SQLite database"""
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
    """Class that defines the state in which variables are held relating to user management"""
    users: list[User] = []  # To hold the list of users
    message: str = ""        # To display success or error messages

    def fetch_all_users(self):
        """Method to retrieve all usernames in the database"""
        with rx.session() as session:
            # Retrieve all users from the database
            self.users = session.exec(User.select()).all()
            self.message = f"Retrieved {len(self.users)} users."
            print(self.users)

class AddUser(rx.State):
    """Class that enables adding users to the database"""
    username: str
    canvas_hash_id: int
    password: str

    def add_user(self):
        """Method to add a user to the database by starting and commiting an rx.session()"""
        with rx.session() as session:
            session.add(
                User(
                    username=self.username,
                    canvas_hash_id=self.canvas_hash_id,
                    password=self.password
                )
            )
            session.commit()
