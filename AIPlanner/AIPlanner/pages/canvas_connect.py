"""Page to connect user's Canvas account to system.
"""
import reflex as rx
from AIPlanner.pages.login import LoginState


class CanvasConnectState(rx.State):
    """
    Canvas connect state.
    Error handles input for manual tokens and sends data to <class that grabs tasks from Canvas>
    """
    _manual_token: str = ""


    def process_token(self, input_data):
        """
        Takes manual token from input on Connect Canvas page,
        error handles input.
        If input is deemed valid, it's sent to <class that grabs tasks from Canvas>.
        Else, an erorr message is returned to the user so they can try again.
        """

        # Getting the manual token from the data package from the input form
        self._manual_token = input_data.get("manual_token")

        # Checking for invalid or potentially-sql-injection values
        invalid_chars = ["'", ";", "--", "<", ">", "%", "$", "^", "-", "[", "]", "=", "OR", "AND", "DROP TABLE", "@"]

        # Looping through invalid char's; if valid, strip whitespace and continue
        for char in invalid_chars:
            if char in self._manual_token:
                # Invalid input: tell user to try again
                return rx.toast("Invalid manual token. Please try again.")

        # Stripping manual token of leading or trailing whitespace
        self._manual_token = self._manual_token.strip()
        print("Valid token entered")

        # Send manual_token to other function that grabs tasks from Canvas (not sure as a private variable we could have another class)
        # Enter code here

        # Send user back to home page upon successful connection
        print("Successful Canvas connection")
        return rx.redirect("/")


def manual_token_input() -> rx.Component:
    """
    Takes the manual token from user and assigns to variable for other classes to use.
    """
    return rx.card(
        rx.form(
            rx.vstack(
                rx.input(
                    placeholder="Enter Canvas manual token",
                    name="manual_token",
                    required=True,
                ),
            ),
            rx.button("Enter", type="submit"),
            on_submit=CanvasConnectState.process_token
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
