"""Page to connect user's Canvas account to system.
"""
import reflex as rx


@rx.page(route="/canvas_connect")
def canvas_connect() -> rx.Component:
    """
    Main function that returns the foundations for the Canvas_Connect page.
    Includes a button that takes user back to home page.
    """
    return rx.container(
        rx.heading("Connect your Canvas account!"),
        rx.text("More coming soon!"),
        rx.link(
            rx.button("Go back"),
            href="/",
            is_external=False,
        ),
    )

# Eof