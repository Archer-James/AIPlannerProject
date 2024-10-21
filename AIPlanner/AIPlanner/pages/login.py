"""Log in page for user.
    Upon successful log in, data is checked in database for account.
    If account found, user redirected to home screen.
    If account not found, show generic error message that does not compromise user privacy.
"""

# import time
import reflex as rx
from rxconfig import config
from AIPlanner.classes.database import AddUser
# import AIPlanner.classes.user as user **Discuss in meeting, fix SignupState and other problems in this file**
import AIPlanner.classes.database as database
# import AIPlanner.pages.processing as processing **Discuss in meeting**


class LoginState(rx.State):
    """
    Login state.
    """
    email: str = ""
    password: str = ""
    # processing_msg: str = "idle"
    # is_processing: bool = False


    def search_for_user(self, login_data):
        """
        Searches for user in database.
        If no user found, returns error statement.
        If user found, user redirected to home page.
        """
        # Getting data from log in form
        self.email = login_data.get('email')
        self.password = login_data.get('password')
        
        # Starting rx database session
        with rx.session() as session:
            user_found = session.exec(
                database.User.select().where(
                    database.User.username == self.email,
                    database.User.password == self.password,
                ),
            ).first()

        # If user found, allow log in
        if user_found:
            print(f"User found: {user_found.username}, {user_found.password}, {user_found.canvas_hash_id}")
            # Doesn't like tasks...
            return rx.redirect('/')

        # User not found
        else:
            return rx.toast("User not found with this email and password combination.")


def login_form() -> rx.Component:
    """
    Login form page that allows the user to enter their email and password and click Log in
    """
    return rx.card(
        rx.form(
            rx.hstack(
                # rx.image(src='/pages/images/tangled_angel_guy.jpg'),
                rx.vstack(
                    rx.heading("Log In!"),
                    rx.text("Log into your account to access your data :)"),
                ),
            ),
            rx.vstack(
                rx.text(
                "Email",
                rx.text.span("*", color="crimson"),
            ),
                rx.input(
                    placeholder="Enter email address *",
                    name="email",
                    type="email",
                    required=True,
                ),
            ),
            rx.vstack(
                rx.text(
                "Password",
                rx.text.span("*", color="crimson"),
                ),
                rx.input(
                    placeholder="Enter password *",
                    name="password",
                    type="password",
                    required=True,
                ),
            ),
            rx.button("Enter", type="submit"),
            on_submit=LoginState.search_for_user,
            #reset_on_submit=True,
        ),
        #rx.text(f"{SignupState.set_processing_msg}"),
        #rx.text(f"Status: {SignupState.change_processing_msg}"),
        spacing="50",
        justify="center",
    )


def login() -> rx.Component:
    """Base page for log in component"""
    return rx.container(
        #render_signup_form(),
        login_form(),
        rx.link(
            rx.button("Go back"),
            href="/",
            is_external=False,
            position="top-right",
            ),
        rx.heading("Don't have an account?"),
        rx.link(
            rx.button("Make an account instead"),
            href="/signup",
            is_external=False,
            position="top-right",
        ),
        width="100%",
        height="100vh",
        padding="2em",
        # bg="grey", # Background
    )

#Eof