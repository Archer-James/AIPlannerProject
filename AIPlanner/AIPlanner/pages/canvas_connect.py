"""Page to connect user's Canvas account to system.
"""
import reflex as rx
from AIPlanner.pages.login import LoginState


def check_if_logged_in():
    """
    Checks if user is logged in.
    Technecly, checks if the username exists as a state (global) variable.

    returns True if username exists (user logged in), false otherwise.
    """
    return rx.cond(
        LoginState.username,
        True, # If username exists (logged in)
        False # Username doesn't exist (not logged in))
    )


def show_log_in_first():
    """
    Shows a log in button, a sign up button, or a continue button to the manual token enter page.
    User can choose which page they want to redirect to.
    """
    return rx.vstack(
        # Log in first button
        rx.link(
            rx.button("Log in first to save Canvas entries"),
            href="/login",
            is_external=False,
        ),
        rx.heading("--- Or ---"),
        # Sign up button
        rx.link(
            rx.button("Sign Up"),
            href="/signup",
            is_external=False,
        ),
        rx.heading("--- Or ---"),
        # Continue without account button
        rx.link(
            rx.button("Continue without account"),
            href="/manualtokens_connect_page",
            is_external=False,
        ),
        spacing="50px",
        justify="center",
    )


def manual_token_input() -> rx.Component:
    """
    Takes the manual token from user and assigns to variable for other classes to use.
    """
    return rx.card(
        rx.hstack(
            rx.form(
                rx.input(
                    placeholder="Enter Canvas manual token here",
                    name="manual_token",
                    required=True,
                ),
            ),
            rx.button("Enter", type="submit"),
            #on_submit=CanvasTokenState.get_tasks_from_token,
        ),
    )


@rx.page(route="/manualtokens_connect_page")
def manualtokens_connect_page():
    """
    Base page for where the user can enter their manual token to connect Canvas.
    Includes an input box for the manual token, error handling and input verification,
    a link to instructions on creating a manual token with Instructure, 
    and a Go Back button that takes the user to the home page.
    """
    return rx.container(
        rx.heading("Enter Canvas Manual Token", size="8"),

        # Have input & check input for errors
        manual_token_input(),
        
        rx.vstack(
            rx.hstack(
                rx.heading("Don't know how?"),
                rx.link(
                    rx.button("Instructions (opens link)"),
                    href="https://community.canvaslms.com/t5/Canvas-Basics-Guide/How-do-I-manage-API-access-tokens-in-my-user-account/ta-p/615312",
                    is_external=True,
                ),
            ),
            rx.link(
                rx.button("Go back"),
                href="/",
                is_external=False,
            ),
        ),
    )



@rx.page(route="/canvas_connect")
def canvas_connect() -> rx.Component:
    """
    Main function that returns the foundations for the Canvas_Connect page.
    Includes a button that takes user back to home page.
    """
    return rx.container(
        rx.heading("Connect your Canvas account!", size="8"),
        rx.vstack(
            rx.cond(
                check_if_logged_in(), # Checking if user is logged in
                manualtokens_connect_page(), # Take user to connect canvas if logged in
                show_log_in_first() # Show option to log in first if not logged in
            ),
            rx.link(
                rx.button("Go back"),
                href="/",
                is_external=False,
            ),
        ),
        width="100%",
        height="100vh",
        padding="2em",
        spacing="4",
        justify="center",
    )

# Eof
