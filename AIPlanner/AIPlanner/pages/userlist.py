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
            lambda user: rx.text(user.username, " ", user.canvas_hash_id, " ", user.id)
        )
    )

def display_user_tasks(state=UserManagementState):
        """Function to display all tasks for a given user"""
        return rx.vstack(
               rx.text("All tasks for user:")
               
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
        display_usernames(),
        rx.logo(),
    )

#Eof
