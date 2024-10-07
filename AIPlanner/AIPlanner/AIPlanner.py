"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from rxconfig import config

# Importing pages
from AIPlanner.pages.signup import signup # Sign up page


#to run test environment
#>cd AIPlanner
#>py -3 -m venv .venv
#>reflex run
# open http://localhost:3000/


class State(rx.State):
    """The app state."""

    ...


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Welcome to Reflex!", size="9"),
            rx.text(
                "Get started by editing ",
                rx.code(f"{config.app_name}/{config.app_name}.py"),
                size="5",
            ),
            rx.link(
                rx.button("Clicks!"),
                href="https://reflex.dev/docs/getting-started/introduction/",
                is_external=True,
            ),
            rx.link(
                rx.button("Sign Up!"),
                href="/signup",
                is_external=False,
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
        rx.logo(),
    )


app = rx.App()
app.add_page(index)


# Megdalia Bromhal - 30 Sept. 2024
# Adding a signup page (as defined in pages.signup)
app.add_page(signup)

if __name__ == "__main__":
    app.run()
# Eof