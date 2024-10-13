"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx


# from pages.signup import signup  # Sign up page

from AIPlanner.CreateCal import GenCalendar


# to run test environment
# >cd AIPlanner
# >py -3 -m venv .venv
# >reflex run
# open http://localhost:3000/


class State(rx.State):
    """The app state."""

    ...

def index() -> rx.Component:
    # Home Page - Calendar
    return rx.center(
        calendar_component(),
        padding="50px",
        
    )

month_year = GenCalendar.get_month_year_label

def calendar_component():
    return rx.vstack(
        # Display current month and year
        rx.button("Load Calendar", on_click=GenCalendar.init_calendar),
        # Navigation buttons for previous and next months
        
        rx.hstack(
            rx.button("Previous", on_click=GenCalendar.prev_month),
            rx.button("Next", on_click=GenCalendar.next_month),
        ),

        # Create the table for the calendar
        rx.heading(GenCalendar.label, size = "lg"),
                # Table header for days of the week
        rx.table.root(
            
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("Sun", scope = "col"),
                    rx.table.column_header_cell("Mon",scope = "col"),
                    rx.table.column_header_cell("Tues",scope = "col"),
                    rx.table.column_header_cell("Wed",scope = "col"),
                    rx.table.column_header_cell("Thurs",scope="col"),
                    rx.table.column_header_cell("Fri",scope = "col"),
                    rx.table.column_header_cell("Sat",scope = "col"),
                    )
                ),
            
                # Table body for days in the month
            rx.table.body(
                rx.foreach(GenCalendar.dates, lambda week: rx.table.row(
                    rx.foreach(week, lambda day: rx.table.cell(day, text_align="center", padding="10px"))
    ))),
        ),
        width="100%",
    
            padding="20px",
        ),
        
    





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