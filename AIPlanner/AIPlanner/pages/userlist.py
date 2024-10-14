"""userlist script

Displays users in the database.
"""

import reflex as rx
from AIPlanner.classes.database import *


def display_users(state: UserManagementState):
    """
    For each user in the database, return their username and canvas hash id.
    If no users found, return "No users found"
    """
    user_data = state.get_user_data()  # Get user data

    # Prepare the list of components
    components = [rx.text(state.message)]  # Start with the message

    # Ensure we handle user_data correctly by ensuring it's a list
    if isinstance(user_data, list):
        for user in user_data:
            user_text = rx.text(f"Username: {user['username']}, Canvas Hash ID: {user['canvas_hash_id']}")
            components.append(user_text)  # Add each rx.text component to the list
    else:
        components.append(rx.text("No users found."))  # Handle the case where user_data isn't valid

    return rx.vstack(*components)  # Create a vstack from the components list


def userlist(state=UserManagementState) -> rx.Component:
    """
    Calls display_users to display all users in database.
    """

    # User list debugging page 
    return rx.container(
        rx.heading("User List", size="0"),
        rx.button("Fetch All Users", on_click=lambda: state.fetch_all_users()),  # Button to fetch users
        display_users(state),
        rx.logo(),
        spacing="5",
        justify="center",
        min_height="85vh",
    )

#Eof
