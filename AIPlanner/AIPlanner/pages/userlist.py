import reflex as rx
from AIPlanner.classes.database import *

def display_usernames(state=UserManagementState):
        return rx.vstack(
        rx.text(state.message),  # Display number of users retrieved
        rx.foreach(  # Use rx.foreach for list rendering
            state.users, 
            lambda user: rx.text(user.username)  # Create a text component for each username
        )
    )

def userlist(state=UserManagementState) -> rx.Component:

    # User list debugging page 
    return rx.container(
        rx.heading("User List", size="0"),
        rx.button("Fetch All Users", on_click=lambda: state.fetch_all_users()),  # Button to fetch users
        display_usernames(state),
        rx.logo(),
    )