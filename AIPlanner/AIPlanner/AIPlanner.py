"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from rxconfig import config
from reflex_calendar import calendar

#from pages.signup import signup  # Sign up page


# to run test environment
# >cd AIPlanner
# >py -3 -m venv .venv
# >reflex run
# open http://localhost:3000/


class State(rx.State):
    """The app state."""

    ...


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.fragment(
        rx.el.style(
            """
        body {
            font-family: Arial, sans-serif;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            width: 14.28%; /* 7 columns */
            border: 1px solid #ddd;
            padding: 10px;
            text-align: center;
        }
        th {
            background-color: #f2f2f2;
        }
        td {
            height: 100px;
            vertical-align: top;
        }
        .empty {
            background-color: #f9f9f9;
        }
    """
        ),
        rx.box(
            rx.heading(id="monthYear", as_="h1", size="8"),
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Sun"),
                        rx.table.column_header_cell("Mon"),
                        rx.table.column_header_cell("Tue"),
                        rx.table.column_header_cell("Wed"),
                        rx.table.column_header_cell("Thu"),
                        rx.table.column_header_cell("Fri"),
                        rx.table.column_header_cell("Sat"),
                    )
                ),
                rx.table.body(id="calendarBody"),
            ),
            
        ),
    )


def signup() -> rx.Component:
    # Signup page
    return rx.container(
        rx.vstack(
            rx.heading("Sign Up!", size="0"),
            rx.input(placeholder="Enter email address", size='lg'),
            rx.input(placeholder="Enter password", type="password", size='lg'),
            rx.button("Submit"),  # on_click=lambda: print("Signed up!")
            rx.link(
                rx.button("Go back"),
                href="/",
                is_external=False,
            ),
            spacing="5",
            justify="center",
            min_height="85vh"
        ),
        rx.logo()
    )




app = rx.App()
app.add_page(index)

# Megdalia Bromhal - 30 Sept. 2024
# Adding a signup page (as defined in pages.signup)
app.add_page(signup)

if __name__ == "__main__":
    app.run()
# Eof
