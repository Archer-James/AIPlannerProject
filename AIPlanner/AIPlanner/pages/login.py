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
    Login state that handles which user is logged in.

    Attributes:
    email (str): email of user.
    password (str): user's password.
    username (str): username of user, which is the user's email before the '@'.
    user_id (int): the user's id number used to identify the user's tasks.
    """

    # Init isn't really great for using the variables across states...
    # def __init__(self, email=str, password=str, username=str, user_id=int):
    #     """
    #     Initialization function for LoginState.
    #     Includes email, password, username (shortened email), and user_id as created in database.
    #     """
    #     self.email = email
    #     self.password = password
    #     self.username = username
    #     self.user_id = user_id

    email: str = ""
    password: str = ""
    username: str
    user_id: int = 0

    def get_email(self):
        """
        Gets the user's email.

        Returns:
        str: user's email
        """
        return self.email


    def get_password(self):
        """
        Gets the user's password.

        Returns:
        str: user's password.
        """
        return self.password


    def get_username(self):
        """
        Gets the user's username.

        Returns:
        str: user's username.
        """
        return self.username


    def get_user_id(self):
        """
        Gets the user's id.

        Returns:
        int: user's int.
        """
        return self.user_id


    def set_email(self, new_email=str):
        """
        Sets the user's email.

        Parameters:
        str: user's email.
        """
        self.email = new_email


    def set_password(self, new_password=str):
        """
        Sets the user's password.

        Parameters:
        str: user's password.
        """
        self.password = new_password


    def set_username(self, new_username=str):
        """
        Sets the user's username.

        Parameters:
        str: user's username.
        """
        self.username = new_username


    def set_user_id(self, new_id=int):
         """
        Sets the user's id.

        Parameters:
        int: user's id.
        """
        self.user_id = new_id

    # processing_msg: str = "idle"
    # is_processing: bool = False

    def direct_to_login(self):
        """
        Uses LoginState to redirect user to the login page.

        Returns:
        Reflex redirect the user to the Login page.
        """
        return rx.redirect("/login")


    def logout(self):
        """
        Uses the LoginState to log out the user.
        Resets the State (class)'s attributes, prints the username (should be empty).
        
        Returns:
        Reflex redirect user to home page.
        """
        self.reset() #Does same as self.username = None
        print(f"Username: {self.username} (should be empty string), User id: {self.user_id}")
        return rx.redirect("/")


    @rx.var
    def display_username(self) -> str:
        """
        Returns:
        str: Determines what to send to home screen depending on if user is logged in.
        If user is logged in, send "Hello {username}!" to the home screen.
        Else, send an empty string.
        """
        return f"Hello {self.username}!" if self.username else ""


    def search_for_user(self, login_data):
        """
        Searches for user in database.
        If no user found, returns error statement.
        If user found, user redirected to home page.

        Parameters:
        login_data (Type?): the login data the user entered into the system's UI.

        Returns:
        Reflex redirect to home page if user found.
        Reflex gives user error if no user found.
        Reflex gives user error if other issues.
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

                # Adding User ID as a variable so we can get tasks assigned to user
                #database.UserManagementState.set_user_id(user_found.id) # I don't think I need to add this, because I'm
                # Getting the user id from the UserManagementState, which means it's already set to whatever the id is.
                self.user_id = user_found.id

                print(f"Username: {self.username}, user id: {self.user_id}")
                # database.UserManagementState.get_user_id

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
    Returns:
    Login form page that allows the user to enter their email and password and click Log in.
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
    """
    Returns:
    Base page for log in component.
    """
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
