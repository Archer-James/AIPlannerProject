"""Success page for successful sign up.

When user signs up successfully, they are taken here.
There's a back button that takes the user back to the home screen.

"""

import reflex as rx


def render_success_page():
    """
    Returns:
    Success page with the back to home button that takes the user to home page.
    """
    return rx.card(
        rx.form(
            rx.vstack(
                rx.hstack(
                    # rx.image(src='/pages/images/tangled_angel_guy.jpg'),
                    rx.vstack(
                        rx.heading("Success!"),
                        rx.text("Please return to the home page"),
                        rx.link(
                            rx.button("Back to Home"),
                            href='/',
                            is_external=False,
                        ),
                    ),
                ),
                rx.text(" -" * 25),
                rx.text("Making sure user is added to database; will remove for final app"),
                rx.link(
                    rx.button("Show all users"),
                    href='/userlist',
                    is_external=False,
                )
            ),
        ),
    )


def success() -> rx.Component:
    """
    Returns:
    Base success page that calls render_success_page() to show button and text.
    """
    return rx.center(
        render_success_page(),
        width="100%",
        height="100vh",
        padding="2em",
    )

#Eof
