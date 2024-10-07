# Importing necessary modules
import reflex as rx


class SignupState(rx.State):
    email: str = ""
    password: str = "" # Passwords are usually strings in web development, apparently
    processing: bool = False


    def submit(self):
        self.processing = True

        # Processing logic here, where we would sign up user
        # User = database user
        # Email and password stored into database

        if (self.email == "") or (self.password == ""):
            print("Invalid info entered. Not processed.")
        else:
            print(f"Processing sign up with email {self.email} and password {self.password}") # Not sure if this will show to user / just terminal
        
        # Reset processing back to False
        self.processing = False
    

    @rx.var
    def processing_msg(self) -> str:
        # Computed var that updates automatically when state changes
        if self.processing == True:
            return "Processing..."
        else:
            return ""


def signup() -> rx.Component:
    # Signup page 
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Sign Up!", size="7"),
            rx.input(
                placeholder="Enter email address", 
                size='lg',
                #value=SignupState.email, # Setting the value the user enters as a state variable (stores it)
                #on_change=lambda e: SignupState.email.set(e.value), # Reacts to user's input real time?
                ),
            rx.input(
                placeholder="Enter password", 
                type="password", 
                size='lg',
                value=SignupState.password,
                on_change=SignupState.password,
                ),
            rx.button(
                "Submit", 
                on_click=SignupState.submit,
                ), 
            rx.text(SignupState.processing_msg),
            rx.link(
                rx.button("Go back"),
                href = "/",
                is_external=False,
            ),
            spacing="5",
            justify="center",
            min_height="85vh"
        ),
        rx.logo()
    )