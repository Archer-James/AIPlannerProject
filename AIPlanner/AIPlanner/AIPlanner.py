"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from rxconfig import config

# Importing pages
from AIPlanner.pages.signup import signup # Sign up page
from AIPlanner.pages.processing import processing # Processing page used in sign up page
from AIPlanner.pages.success import success # Success page shown after successful sign up
from AIPlanner.classes.database import * # Database
from AIPlanner.pages.userlist import userlist # Userlist debugging page


# from pages.signup import signup  # Sign up page

from AIPlanner.CreateCal import GenCalendar


# to run test environment
# >cd AIPlanner
# >py -3 -m venv .venv
# >reflex run
# open http://localhost:3000/


class State(rx.State):
    """The app state."""
    task_name: str = ""
    task_description: str = ""
    priority: str = "Medium"
    date_time: str = ""
    show_error: bool = False

    # Need to connect this with database
    def apply_task(self):
        """
        Apply task button that will give errors if there are missing required fields
        Will also reset after successful apply
        """
        if not self.task_name.strip():
            self.show_error = True
        else:
            self.show_error = False
            print(f"Task applied: {self.task_name, self.task_description, self.priority, self.date_time}")
            self.task_name = ""
            self.task_description = ""
            self.priority = "Medium"
            self.date_time = ""

    def set_task_name(self, task_name: str):
        """
        Setter for the task name
        """
        self.task_name = task_name
        if self.task_name.strip():
            self.show_error = False

    def set_task_description(self, task_description: str):
        """
        Setter for task description
        """
        self.task_description = task_description

    def set_priority(self, priority: str):
        """
        Setter for priority
        """
        self.priority = priority

    def set_date_time(self, date_time: str):
        """
        Setter for date time
        """
        self.date_time = date_time

    ...

def task_input_form():
    """
    Task bar initializer that has task name, task description, priority, set date/time, and apply
    """
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.input(
                    placeholder="Task Name",
                    on_change=State.set_task_name,
                    value=State.task_name,
                    flex=1,
                    #border_right="2px solid #E2E8F0",
                    #border_left="2px solid #E2E8F0",
                ),
                rx.input(
                    placeholder="Task Description",
                    on_change=State.set_task_description,
                    value=State.task_description,
                    flex=1,
                    #border_right="2px solid #E2E8F0",
                    #border_left="2px solid #E2E8F0",
                ),
                rx.select(
                    ["Low", "Medium", "High"],
                    placeholder="Priority: Medium",
                    on_change=State.set_priority,
                    value=State.priority,
                    flex=1,
                    #border_right="2px solid #E2E8F0",
                    #border_left="2px solid #E2E8F0",
                ),
                rx.input(
                    placeholder="Set Date/Time",
                    type_="datetime-local",
                    on_change=State.set_date_time,
                    value=State.date_time,
                    flex=1,
                    #border_left="2px solid #E2E8F0",
                    #border_right="2px solid #E2E8F0",
                ),
                rx.button("Apply Task", on_click=State.apply_task, flex=1),
                spacing="0",
                #border="2px solid #E2E8F0",
                border_radius="md",
            ),
            rx.cond(
                    State.show_error,
                    rx.text("Task name is required", color="red", font_size="sm"),
            ),
            align_items = "stretch",
        ),
        width="100%",
    )

def index() -> rx.Component:
    """
    Home page of AIPlanner.
    """
    # Welcome Page (Index)
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.hstack(
            rx.link(
                rx.button("Sign Up!"),
                href="/signup",
                is_external=False,
            ),
            rx.link(
                rx.button("Show All Users"),
                href="/userlist",
                is_external=False,
            ),
            task_input_form(),
            spacing="5",
            justify="center",
            min_height="15vh", # Squishing it up a tad so we can see the giant text

        ),
    ), rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("AIPlanner Home Page", size="9"),
            rx.text(
                "More coming soon! Currently coding ",
                rx.code(f"{config.app_name}/{config.app_name}.py"),
                size="5",
            ),
            rx.center(
            calendar_component(),

            spacing="5",
            justify="center",
            min_height="50vh", # Changing to 50 to squish it up more
        ),

        padding="50px",
    )
    ),





month_year = GenCalendar.get_month_year_label

def calendar_component():
    """
    Calendar initializer and caller
    """
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



app = rx.App(
    theme=rx.theme(
        appearance="light",
        has_background=True,
        radius="large",
        accent_color="pink",
        panel_background="translucent",
    )
)
app.add_page(index)



# Megdalia Bromhal - 30 Sept. 2024
# Adding a signup page (as defined in pages.signup)
app.add_page(signup)
# Adding processing page (used in sign up page)
app.add_page(processing)
# Adding success page (used in sign up page)
app.add_page(success)
# Adding debugging user list page
app.add_page(userlist)
# Adding a signup page, alternative, **Discuss in meeting**
#app.add_page(signup, on_load=UserManagementState.fetch_all_users)


if __name__ == "__main__":
    app.run()
# Eof
