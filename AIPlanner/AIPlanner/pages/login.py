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


def check_passwords(password, password_check):
    """
    Checks if password is the same as the password check.

    param password: rx password         the password the user enters
    param password_check: rx password   the password the user enters into the check
    returns True if passwords match, False otherwise
    """
    if password == password_check:
        return True
    else:
        return False


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

        # Iterating through Reflex database
        # for user in database.UserManagementState.users:
        #     if (user.username == self.email) and (user.password == self.password):
        #         user_found = True
        #         break
        
        # Starting rx database session
        with rx.session() as session:
            user_found = session.exec(
                database.User.select().where(
                    database.User.username == self.email,
                    database.User.password == self.password,
                ),
            ).first()


        # rx.foreach(database.UserManagementState.users, lambda user: (
        #     user_found := (user.username == self.email) and (user.password == self.password))
        # )

    #     class QueryUser(rx.State):
    # name: str
    # users: list[User]

    # def get_users(self):
    #     with rx.session() as session:
    #         self.users = session.exec(
    #             User.select().where(
    #                 User.username.contains(self.name)
    #             )
    #         ).all()

        # If user found, allow log in
        if user_found:
            print(f"User found: {user_found.username}, {user_found.password}, {user_found.canvas_hash_id}")
            # Doesn't like tasks...
            return rx.redirect('/')

        # User not found
        else:
            return rx.toast("User not found with this email and password combination.")


# def display_usernames(state=UserManagementState):
#         """Function to display usernames"""
#         return rx.vstack(
#         rx.text(state.message),  # Display number of users retrieved
#         rx.foreach(  # Use rx.foreach for list rendering
#             state.users, 
#             lambda user: rx.text(user.username)  # Create a text component for each username
#         )
#     )



    def submit(self, signup_data):
        """
        Function that handles user's data when user signs up. Saves username and password into database.

        param signup_data: data the user enters into the signup form (i.e. username and password)
        """
        self.email = signup_data.get('email')
        self.password = signup_data.get('password')
        self.password_check = signup_data.get('password_check')
        
        # Checking if password matches password check
        if check_passwords(self.password, self.password_check) == True:
            
            # Checking that email is only 25 chars long max
            if len(self.email) <= 25:
                # Passwords match, so process account
                print("Processing new account.")
                #self.is_processing = True
                #self.change_processing_msg()
                # time.sleep(4)
                # Need processing message!!!

                # Adding account to database
                try:
                    # Create a new user with Reflex database
                    database.create_user(username=self.email, canvas_hash_id=1, password=self.password)
                
                    #self.is_processing = False # Changing back just in case
                    #self.change_processing_msg()

                    print("Account created in rx database")
                    return rx.redirect('/success')

                # If error, tell user to try again
                except ModuleNotFoundError as e:
                    print(e)
                    return rx.toast("Error occurred while saving data. Please try again.")

            # Email is too long; tell user
            else:
                return rx.toast("Email is too long. Please enter appropriate email.")
        
        # If passwords don't match, ask user to re-enter data
        else:
            return rx.toast("Passwords do not match. Please enter information again.")
    
#         # Create a new user with csv testing database
#         new_user, success_code = user.create_user(username=self.email, 
#                                                   canvas_hash_id=None, 
#                                                   password=self.password
#                                                   )
            

    # @rx.var(cache=True) # Cached variable
    # def set_processing_msg(self) -> str:
    #     return f"{self.processing_msg}"


    # @rx.var(cache=True)
    # def change_processing_msg(self) ->str:
    #     return str(self.processing_msg)


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