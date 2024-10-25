"""Log in page for user.
    Upon successful log in, data is checked in database for account.
    If account found, user redirected to home screen.
    If account not found, show generic error message that does not compromise user privacy.

    Also includes log out interactions when user clicks "log out" in home page.
"""

import reflex as rx
import AIPlanner.classes.database as database


class LoginState(rx.State):
    """
    Login state.
    """

    # Should try __init__ function
    email: str = ""
    password: str = ""
    username: str
    # processing_msg: str = "idle"
    # is_processing: bool = False


    def direct_to_login(self):
        """
        Uses LoginState to redirect user to the login page.
        """
        return rx.redirect("/login")


    def logout(self):
        """
        Uses the LoginState to log out the user.
        """
        self.reset() #Does same as self.username = None
        print(f"Username: {self.username} (should be "")")
        return rx.redirect("/")


    @rx.var
    def display_username(self) -> str:
        """
        Determines what to send to home screen depending on if user is logged in.
        If user is logged in, send "Hello {username}!" to the home screen.
        Else, send an empty string.
        """
        return f"Hello {self.username}!" if self.username else ""


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

            try:
                print(f"User found: {user_found.username}, {user_found.password}, {user_found.canvas_hash_id}")

                self.username = user_found.username.split("@")[0]
                print(f"Username: {self.username}")
                # Sending username to set_username to use in home screen
                #LoginState.set_username(user_found.username)

                # Doesn't like tasks...
                return rx.redirect('/')
            
            # Error handling 
            except TypeError as e:
                print(f"Error: {e}")
                return rx.toast("Error logging in, please retry.")

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
    return rx.card(
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