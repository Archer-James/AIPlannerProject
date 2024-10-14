"""Signup page script.

Includes the signup form, which enables users to enter their email and password and click submit.
Clicking submit adds their information as a User object in the database, 
    and takes them to a success page.
The user must click "Go home" from the success page.
User can also go back to the home page.
"""


# Importing necessary modules
import time
import reflex as rx
#import AIPlanner.classes.user as user
import AIPlanner.classes.database as database


class SignupState(rx.State):
    """
    Signup page.
    """
    email: str = ""
    password: str = "" # Passwords are usually strings in web development, apparently
    is_processing: bool = False


    def submit(self, signup_data):
        """
        Function that handles user's data when user signs up. 
        Saves username and password into database.

        param signup_data: data the user enters into the signup form (i.e. username and password)
        """
        self.email = signup_data.get('email')
        self.password = signup_data.get('password')

        # Create a new user with csv testing database
        # new_user, success_code = user.create_user(username=self.email,
        #                                           canvas_hash_id=None,
        #                                           password=self.password
        #                                           )

        # Error handling the submit form
        try:
            self.is_processing = True
            time.sleep(2)
            # Need processing message!!!

            # Create a new user with Reflex database
            database.create_user(username=self.email, canvas_hash_id=1, password=self.password)

            self.is_processing = False

            return rx.redirect('/success')

        # If error, tell user to try again
        except ValueError:
            return rx.toast(str("Error occurred while saving data. Please try again."))


    # @rx.var(cache=True) # Cached variable
    # def set_processing_msg(self) -> str:
    #     return f"{self.processing_msg}"


    # @rx.var(cache=True)
    # def change_processing_msg(self) ->str:
    #     return str(self.processing_msg)


def signup_form() -> rx.Component:
    """
    Signup form page that allows the user to enter their email and password, click submit.
    Clicking submit will send the entered data to the database.
    """
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
            # reset_on_submit=True,
        ),
        rx.vstack(
            #rx.text(f"{SignupState.set_processing_msg}"),
            rx.cond(
                SignupState.is_processing,
                rx.text("Processing...please wait", color="pink"),
                rx.text("Idle")
            ),
        ),
        spacing="50",
        justify="center",
    )


def signup() -> rx.Component:
    """
    The base page for the signup page.
    Includes the signup form component, and the link to go back to the home page.
    """
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
