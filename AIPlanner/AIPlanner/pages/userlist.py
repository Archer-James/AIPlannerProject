"""userlist script

Displays users in the database.
"""
import random
import reflex as rx
from AIPlanner.classes.database import *
import AIPlanner.classes.database as database

def display_usernames(state=UserManagementState):
    """Function to display usernames"""
    return rx.vstack(
    rx.text(state.message),  # Display number of users retrieved
    rx.foreach(  # Use rx.foreach for list rendering
        state.users,
        # Create a text component for each username
            lambda user: rx.text(user.username, " ", user.canvas_hash_id, " ", user.id, user.tasks)
        )
    )

def userlist(state=UserManagementState) -> rx.Component:
    """
    Calls display_usernames to display all users in database, 
    with buttons for quick addition of test users to the database
    and repeated retreival of users from the database
    """
    # User list debugging page
    return rx.container(
        rx.heading("User List", size="0"),
        rx.button("Fetch All Users From Database", on_click=state.fetch_all_users()),
        rx.button("Add Test User",
                     # Button to add test user
                     on_click=lambda: state.add_test_user()),
        rx.button("Add task to test user with ID 1", on_click=lambda: state.add_test_task(2)),
        rx.button("Show tasks assigned to user with ID 1", on_click=lambda: state.get_user_tasks(2)),
        display_usernames(),
        rx.logo(),
    )

#Eof
