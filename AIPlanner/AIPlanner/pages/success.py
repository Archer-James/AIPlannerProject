import reflex as rx


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
    )



def success() -> rx.Component:
    return rx.center(
        render_success_page(),
        width="100%",
        height="100vh",
        padding="2em",
        bg="black", # Background
    )