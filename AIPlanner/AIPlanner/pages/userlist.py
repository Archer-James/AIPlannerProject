import reflex as rx

def userlist() -> rx.Component:
    # User list debugging page 
    return rx.container(
        rx.vstack(
            rx.heading("User List", size="0"),
            spacing="5",
            justify="center",
            min_height="85vh"
        ),
        rx.logo()
    )