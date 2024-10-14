import reflex as rx


def render_processing_msg():
    return rx.card(
        rx.form(
            rx.hstack(
                # rx.image(src='/pages/images/tangled_angel_guy.jpg'),
                rx.vstack(
                    rx.heading("Processing...please stay on page..."),
                ),
            ),
        ),
    )



def processing() -> rx.Component:
    # Signup page 
    return rx.center(
        render_processing_msg(),
        width="100%",
        height="100vh",
        padding="2em",
        bg="blue", # Background
    )