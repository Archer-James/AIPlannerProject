"""Signup page script.

Includes the signup form, which enables users to enter their email and password and click submit.
Clicking submit adds their information as a User object in the database, 
    and takes them to a success page.
The user must click "Go home" from the success page.
User can also go back to the home page.
"""
# Importing necessary modules
import reflex as rx
import AIPlanner.classes.database as database


def check_passwords(password, password_check):
    """
    Checks if password is the same as the password check.

    Parameters:
    password (rx password): the password the user enters
    password_check (rx password): the password the user enters into the check

    Returns:
    True if passwords match, False otherwise
    """
    if password == password_check:
        return True
    else:
        return False


class SignupState(rx.State):
    """
    Signup page.
    
    Attributes:
    email (str): user's email.
    password (str): user's password.
    password_check (str): user's password entered twice to make sure it's the password the user wants
    is_submitting (bool): flag that tracks if the user has clicked "Enter" for the signup form.
    """
    email: str = ""
    password: str = "" # Passwords are usually strings in web development, apparently
    password_check: str = ""
    is_submitting: bool = False


    def direct_to_signup(self):
        """
        Returns:
        Uses the Signup State to redirect users to the signup page.
        """
        return rx.redirect("/signup")


    def submit(self, signup_data:dict):
        """
        Function that handles user's data when user signs up. 
        Saves username and password into database.

        Parameters:
        signup_data (dict): data the user enters into the signup form (i.e. username and password)

        Returns:
        Reflex redirect to home page if account made successfully.
        Reflex error to user if issue with database.
        Reflex error to user if email is too long.
        Reflex error to user if passwords don't match.
        """
        # Setting flag to true to take away submit button
        self.is_submitting = True
        yield

        self.email = signup_data.get('email')
        self.password = signup_data.get('password')
        self.password_check = signup_data.get('password_check')

        # Check to see if someone with email address is already registered
        with rx.session() as session:
            user_already_exists = session.exec(
                database.User.select().where(
                    database.User.username == self.email,
                ),
            ).first()
        print(f"self.email: {self.email}")

        if user_already_exists: # If user already exists, tell user to try with different email
            self.is_submitting = False
            yield rx.toast("Account already exists with this email. Try again with a different email.")

        else:

            # Checking if password matches password check
            if check_passwords(self.password, self.password_check) is True:

                # Checking that email is only 25 chars long max
                if len(self.email) <= 25:
                    # Passwords match, so process account
                    print("Processing new account.")

                    # Adding account to database
                    try:
                        # Create a new user with Reflex database
                        database.create_user(username=self.email,
                                            canvas_hash_id=1, password=self.password)

                        #self.is_processing = False # Changing back just in case
                        #self.change_processing_msg()

                        print("Account created in rx database")
                        self.is_submitting = False
                        return rx.redirect('/success')

                    # If error, tell user to try again
                    except ModuleNotFoundError as e:
                        print(e)
                        self.is_submitting = False
                        yield rx.toast("Error occurred while saving data. Please try again.")

                # Email is too long; tell user
                else:
                    self.is_submitting = False
                    yield rx.toast("Email is too long. Please enter appropriate email.")

            # If passwords don't match, ask user to re-enter data
            else:
                self.is_submitting = False
                yield rx.toast("Passwords do not match. Please enter information again.")


def signup_form() -> rx.Component:
    """
    Returns:
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
            rx.button(
                "Submit", 
                type="submit",
                disabled = SignupState.is_submitting,
            ),
            on_submit=SignupState.submit,
            # reset_on_submit=True,
        ),
        #rx.text(f"{SignupState.set_processing_msg}"),
        #rx.text(f"Status: {SignupState.change_processing_msg}"),
        spacing="50",
        justify="center",
    )

def signup() -> rx.Component:
    """
    Returns:
    The base page for the signup page.
    Includes the signup form component, and the link to go back to the home page.
    """
    # Signup page
    return rx.container(
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
        # bg="grey", # Background
    )

#Eof
