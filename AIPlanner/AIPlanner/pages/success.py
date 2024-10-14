import reflex as rx
import AIPlanner.pages.userlist as Userlist
import AIPlanner.classes.database as database


def render_success_page():
    return rx.card(
        rx.form(
            rx.hstack(
                # rx.image(src='/pages/images/tangled_angel_guy.jpg'),
                rx.vstack(
                    rx.heading("Success!"),
                    rx.text("Please return to the home page")
                ),
                rx.link(
                    rx.button("Back to Home"),
                    href='/',
                    is_external=False,
                ),
            ),
        ),
        rx.text(" -" * 25),
        rx.text("Making sure user is added to database; will remove for final app"),
        Userlist.userlist(),
    )



def success() -> rx.Component:
    return rx.center(
        render_success_page(),
        width="100%",
        height="100vh",
        padding="2em",
        bg="black", # Background
    )