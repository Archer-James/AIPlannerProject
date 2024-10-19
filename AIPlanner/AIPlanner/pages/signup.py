# Importing necessary modules

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


class SignupState(rx.State):
    """
    Signup page.
    """
    email: str = ""
    password: str = "" # Passwords are usually strings in web development, apparently
    password_check: str = "" # We make the user enter their password twice so they can make sure it's correct
    processing_msg: str = "idle"
    is_processing: bool = False


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


def signup_form() -> rx.Component:
    """Signup form page that allows the user to enter their email and password and click Submit"""
    return rx.card(
        rx.form(
            rx.hstack(
                # rx.image(src='/pages/images/tangled_angel_guy.jpg'),
                rx.vstack(
                    rx.heading("Sign Up!"),
                    rx.text("Make an account with us to save your data and access it later :)"),
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
                rx.text("Confirm password",
                        rx.text.span("*", color="crimson")
                ),
                rx.input(
                    placeholder="Confirm password *",
                    name="password_check",
                    type="password",
                    required=True,
                ),
            ),
            rx.button("Submit", type="submit"),
            on_submit=SignupState.submit,
            reset_on_submit=True,
        ),
        #rx.text(f"{SignupState.set_processing_msg}"),
        #rx.text(f"Status: {SignupState.change_processing_msg}"),
        spacing="50",
        justify="center",
    )

def signup() -> rx.Component:
    """Base page for signup component"""
    # Signup page 
    return rx.container(
        #render_signup_form(),
        signup_form(),
        rx.link(
            rx.button("Go back"),
            href="/",
            is_external=False,
            position="top-right",
            ),
        width="100%",
        height="100vh",
        padding="2em",
        bg="grey", # Background
    )

#Eof