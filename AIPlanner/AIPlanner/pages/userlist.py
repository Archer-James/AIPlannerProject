import reflex as rx
from AIPlanner.classes.database import *

def display_usernames(state=UserManagementState):
        """Function to display usernames"""
        return rx.vstack(
        rx.text(state.message),  # Display number of users retrieved
        rx.foreach(  # Use rx.foreach for list rendering
            state.users, 
            lambda user: rx.text(user.username)  # Create a text component for each username
        )
    )

def display_user_tasks(state=UserManagementState):
        """Function to display all tasks for a given user"""
        return rx.vstack(
               rx.text("All tasks for user:")
               
        )
def userlist(state=UserManagementState) -> rx.Component:
    """Function to display user list"""
    # User list debugging page 
    return rx.container(
        rx.heading("User List", size="0"),
        rx.button("Fetch All Users", on_click=lambda: state.fetch_all_users()),  # Button to fetch users
        display_usernames(state),
        rx.button("Get all user tasks", on_click=lambda: state.get_user_tasks(1)), # Button to get user tasks (temporarily hardcoded 1 as user id, integrate with login later)
        rx.logo(),
    )
