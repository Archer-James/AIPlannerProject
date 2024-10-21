"""Processing page.

User is taken to this page, which has no buttons or interactive objects, 
    when processing sign up data.
Once processing is complete, user is taken to new page.

"""

import reflex as rx


def render_processing_msg():
    """Page with "processing" text."""
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
    """
    Base function for processing page.
    Calls render_processing_msg() for text
    """
    # Signup page 
    return rx.center(
        render_processing_msg(),
        width="100%",
        height="100vh",
        padding="2em",
        bg="blue", # Background
    )

#Eof
