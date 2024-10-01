# Megdalia Bromhal
# 30 Sept. 2024

# Importing necessary modules
import reflex as rx

def signup() -> rx.Component:
    # Signup page 
    return rx.container(
        rx.vstack(
            rx.heading("Sign Up!", size="0"),
            rx.input(placeholder="Enter email address", size='lg'),
            rx.input(placeholder="Enter password", type="password", size='lg'),
            rx.button("Submit", on_click=lambda: print("Signed up!")),
            spacing="5",
            justify="center",
            min_height="85vh"
        ),
        rx.logo()
    )