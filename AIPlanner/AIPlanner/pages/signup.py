# Importing necessary modules
import reflex as rx
import AIPlanner.classes.user as user
import AIPlanner.classes.database as database
import AIPlanner.pages.processing as processing


class SignupState(rx.State):
    """
    Signup page.
    """
    email: str = ""
    password: str = "" # Passwords are usually strings in web development, apparently
    processing: bool = False


    def submit(self, signup_data):
        """
        Function that handles user's data when user signs up. Saves username and password into database.

        param signup_data: data the user enters into the signup form (i.e. username and password)
        """
        self.email = signup_data.get('email')
        self.password = signup_data.get('password')

        self.processing = True
            
        # Create a new user with csv testing database
        new_user, success_code = user.create_user(username=self.email, canvas_hash_id=None, password=self.password)
        
        # Error handling the submit form
        try:
            
            # Need processing message!!!
            is_processing = True

            # Create a new user with Reflex database
            database.create_user(username=self.email, canvas_hash_id=1, password=self.password)

            return rx.redirect('/success')
        
        # If error, tell user to try again
        except Exception:
            return rx.toast(f"Error occurred while saving data. Please try again.")


# Make a dynamic variable to show processing  
# @rx.var(cache=True)
# def processing_msg():
#     return ["Processing...Please stay on page." if is_processing else ""]

        # print(database.UserManagementState.fetch_all_users())
        # print(database.UserManagementState.get_user_data())

        # If error message throughout saving process, tells user, otherwise says successful
        # if success_code == 0:
        #     print("Success")
        #     #return rx.toast(f"Success! Please go to home page")
        #     return rx.redirect("/success")
        # elif success_code == 1:
        #     print("Error saving data")
        #     return rx.toast(f"Error in saving data. Please try again.")
            # Unfortunately right now with filename errors it just makes a new file and writes to that..

            # return rx.redirect("/processing")
        
    # def processing_page(self) -> rx.Component:
    #     return rx.card(
    #         rx.vstack(
    #             rx.text("Processing...please stay on page")
    #         )
    #     )

    # @rx.var
    # def processing_msg(self) -> str:
    #     # Computed var that updates automatically when state changes
    #     if self.processing == True:
    #         return "Processing..."
    #     else:
    #         return "Submit!"


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
        # rx.text(msg=processing_msg()),
        spacing="50",
        justify="center",
    )


# def render_user_entries(title: str):
#     return rx.vstack(
#         rx.text(title, color="gray", font_size="11px", weight="bold"),
#         #rx.chakra.input(),
#         width="100%",

#     )


# def render_signup_form():
#     return rx.vstack(
#         rx.hstack(
#             rx.icon(tag="lock", size=28, color="rgba(127, 127, 127, 1)"),
#             width="100%",
#             height="55px",
#             bg="#181818",
#             border_radius="10px 10px 0px 0px",
#             display="flex",
#             justify_content="center",
#             align_items="center",

#         ),
#         rx.vstack(
#             render_user_entries("Enter email address"),
#             width="100%",
#             padding=""
#         ),
#         width=["100%", "100%", "65%", "50%", "35%"],
#         bg="rgba(21, 21, 21, 0.55)",
#         border="0.75px solid #2e2e2e",
#         border_radius="10px",
#         box_shadow="0px 8px 16px 6px rgba(0, 0, 0, 0.25)",

#     )


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
    # return rx.container(
    #     rx.color_mode.button(position="top-right"),
    #     rx.vstack(
    #         rx.heading("Sign Up!", size="7"),
    #         rx.input(
    #             placeholder="Enter email address", 
    #             size='lg',
    #             #value=SignupState.email, # Setting the value the user enters as a state variable (stores it)
    #             #on_change=lambda e: SignupState.email.set(e.value), # Reacts to user's input real time?
    #             ),
    #         rx.input(
    #             placeholder="Enter password", 
    #             type="password", 
    #             size='lg',
    #             value=SignupState.password,
    #             #on_change=SignupState.password,
    #             ),
    #         rx.button(
    #             "Submit", 
    #             on_click=SignupState.submit,
    #             ), 
    #         rx.text(SignupState.processing_msg),
    #         rx.link(
    #             rx.button("Go back"),
    #             href = "/",
    #             is_external=False,
    #         ),
    #         spacing="5",
    #         justify="center",
    #         min_height="85vh"
    #     ),
    #     rx.logo()
    # )