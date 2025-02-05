"""Module containing classes and methods pertaining to the SQLite database built into Reflex"""
from datetime import date, time, timedelta
from typing import List, Optional
import random
from AIPlanner.pages.login import LoginState

import reflex as rx
import sqlmodel

class User(rx.Model, table=True):
    """Class that defines the User table in the SQLite database
    
    Attributes:
    username: A unique string identifier
    canvas_hash_id: Deprecated, no use
    password: A string used to authenticate user login
    id: Automatically generated unique identifier for each user
    tasks: List of tasks for the user, taken from Task table
    """
    username: str
    canvas_hash_id: int
    password: str
    tasks: List["Task"] = sqlmodel.Relationship(back_populates="user")

class Task(rx.Model, table=True):
    """Class that defines the Task table in the SQLite database
    
    Attributes:
    recur_frequency: Integer that determines how frequently a task recurs
    due_date: Date that the task must be completed by
    is_deleted: Boolean that determines whether the task is deleted or not
    task_name: String name of the task
    description: String description of the task
    task_id: Deprecated, no use
    priority_level: Integer between 1 and 3 that determines the level of priority for a task, lower value is higher priority level
    assigned_block_date: Date that the task is assigned to
    assigned_block_start_time: Time that the task should be started on the assigned date
    assigned_block_duration: Timedelta for how long after start time the task should be worked on
    user_id: Integer foreign key reference to the user whose task this is
    user: Populates the tasks field of the User table
    """
    recur_frequency: int
    due_date: date
    is_deleted: bool
    task_name: str
    description: str
    task_id: int
    priority_level: int
    assigned_block_date: Optional[date]
    assigned_block_start_time: Optional[time]
    assigned_block_duration: Optional[timedelta]
    user_id: int = sqlmodel.Field(foreign_key="user.id")
    user: Optional[User] = sqlmodel.Relationship(back_populates="tasks")

    def get_priority_color(self):
        """Return the color string for a given priority."""
        priority = self["priority_level"]  # Access as dictionary
        return rx.match(
            priority,
            (1, "red"),    # High priority
            (2, "blue"), # Medium priority
            (3, "green"),   # Low priority
            "gray"         # Default
        )

class UserManagementState(rx.State):
    """Class that defines the state in which variables and 
    functions are held relating to user management
    
    Attributes:
    users: List of users to hold the result of retrieving all users from the database
    message: String to hold success and error messages for functions in the state
    tasks: List of tasks to hold the result of retrieving tasks from users
    user_id: Integer holding the user.id of the currently logged-in user
    """
    users: list[User] = []  # To hold the list of users
    message: str = ""        # To display success or error messages
    tasks: list[Task] = []
    user_id: int = 1
    editing_task_id_name: Optional[int] = None  # ID of the task currently being edited
    editing_task_id_description: Optional[int] = None
    new_task_name: str = ""  # Temporary storage for the new task name
    new_task_description: str = ""

    def set_user_id(self, user_id: int):
        """Setter method for user ID"""
        self.user_id = user_id

    def get_user_id(self):
        """Getter for user id"""
        return self.user_id

    def __str__(self):
        """
        Returns string version of self.user_id.
        """
        return f"{self.user_id}"

    def get_user_tasks(self, user_id: int):
        """Method to retrieve all tasks for a given user"""
        with rx.session() as session:
            self.tasks = session.exec(
                Task.select().where(Task.user_id == user_id).where(Task.is_deleted.is_(False))
            ).all()
        print("calling")
        print(self.tasks)

    def fetch_all_users(self):
        """Method to retrieve all usernames in the database"""
        with rx.session() as session:
            # Retrieve all users from the database
            self.users = session.exec(User.select()).all()
            self.message = f"Retrieved {len(self.users)} users."
            print(self.users)

    def add_test_user(self):
        """Method to insert test users into the database"""
        create_user("Test", random.randint(850000000,850999999), "test11")

    def add_test_task(self):# user_id
        """Method to add test tasks into the database"""
        new_task = Task(
            recur_frequency=7,  # For example, a weekly recurring task
            due_date=date(2024, 12, 25),
            is_deleted=False,
            task_name="Complete project",
            description="Finish the project for final submission.",
            task_id=1,
            priority_level=2,
            assigned_block_date=date(2024, 12, 24),
            assigned_block_start_time=time(14, 0),  # Start at 2 PM
            assigned_block_duration=timedelta(hours=2),
            user_id = LoginState.user_id #self.user_id
        )
        with rx.session() as session:
            session.add(new_task)
            session.commit()

    def set_editing_task_id_name(self, task_id: Optional[int]):
        """Set the ID of the task being edited."""
        self.editing_task_id_name = task_id

    def set_editing_task_id_description(self, task_id: Optional[int]):
        """Set the ID of the task being edited for its description."""
        self.editing_task_id_description = task_id

    def set_new_task_name(self, value: str):
        """Set the new task name."""
        self.new_task_name = value

    def set_new_task_description(self, value: str):
        """Set the new task description."""
        self.new_task_description = value

    def edit_task_name(self, task_id: int, new_name: str):
        """Update the task name for the given task ID."""
        with rx.session() as session:
            task = session.exec(
                Task.select().where(Task.id == task_id)
            ).first()
            if task:
                task.task_name = new_name
                session.commit()
                print(f"Task name updated to '{new_name}' for task ID: {task_id}.")
            else:
                print(f"No task found with ID: {task_id}.")

    def edit_task_description(self, task_id: int, new_description: str):
        """Update the task description for the given task ID."""
        with rx.session() as session:
            task = session.exec(
                Task.select().where(Task.id == task_id)
            ).first()
            if task:
                task.description = new_description
                session.commit()
                print(f"Task description updated to '{new_description}' for task ID: {task_id}.")
            else:
                print(f"No task found with ID: {task_id}.")

    def delete_task(self, task_id: int):
        """Marks the task as deleted by setting is_deleted to True if it's not already True."""
        with rx.session() as session:
            # Try to get the task with the specified ID
            task = session.exec(
                Task.select().where(Task.id == task_id)
            ).first()
            if task:
                if not task.is_deleted:
                    # Set is_deleted to True and commit
                    task.is_deleted = True
                    session.commit()
                    print(f"Task {task_id} marked as deleted.")
                else:
                    print(f"Task {task_id} is already marked as deleted.")
            else:
                print(f"No task found with ID: {task_id}")

class AddUser(rx.State):
    """Class that enables adding users to the database"""
    username: str
    canvas_hash_id: int
    password: str

    def set_username(self, value: str):
        """Initializing username"""
        self.username = value

    def set_canvas_hash_id(self, value: int):
        """Initializing user canvas ID"""
        self.canvas_hash_id = value

    def set_password(self, value: str):
        """Initializing user's password"""
        self.password = value

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
