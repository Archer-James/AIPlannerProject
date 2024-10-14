# Importing necessary modules

from datetime import time
import reflex as rx
from rxconfig import config
from AIPlanner.classes.database import AddUser
# import AIPlanner.classes.user as user **Discuss in meeting, fix SignupState and other problems in this file**
import AIPlanner.classes.database as database
# import AIPlanner.pages.processing as processing **Discuss in meeting**


class SignupState(rx.State):
    """
    Signup page.
    """
    email: str = ""
    password: str = "" # Passwords are usually strings in web development, apparently
    processing_msg: str = "idle"
    is_processing: bool = False


    def submit(self, signup_data):
         """
         Function that handles user's data when user signs up. Saves username and password into database.

         param signup_data: data the user enters into the signup form (i.e. username and password)
         """
         self.email = signup_data.get('email')
         self.password = signup_data.get('password')
            
#         # Create a new user with csv testing database
#         new_user, success_code = user.create_user(username=self.email, 
#                                                   canvas_hash_id=None, 
#                                                   password=self.password
#                                                   )
        
         # Error handling the submit form
         try:
            
             print("Processing...")
             self.is_processing = True
             #self.change_processing_msg()
            
             time.sleep(4)
             # Need processing message!!!

             # Create a new user with Reflex database
             database.create_user(username=self.email, canvas_hash_id=1, password=self.password)

             self.is_processing = False # Changing back just in case
             self.change_processing_msg()

             return rx.redirect('/success')
        
         # If error, tell user to try again
         except Exception:
             return rx.toast(f"Error occurred while saving data. Please try again.")
        

    @rx.var(cache=True) # Cached variable
    def set_processing_msg(self) -> str:
        return f"{self.processing_msg}"


    @rx.var(cache=True)
    def change_processing_msg(self) ->str:
        return str(self.processing_msg)


def signup_form() -> rx.Component:
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
            ),
            rx.button("Submit", type="submit"),
            on_submit=SignupState.submit,
            reset_on_submit=True,
        ),
        #rx.text(f"{SignupState.set_processing_msg}"),
        rx.text(f"Status: {SignupState.change_processing_msg}"),
        spacing="50",
        justify="center",
    )

def signup() -> rx.Component:
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