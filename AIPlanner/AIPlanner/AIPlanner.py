"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from rxconfig import config

# Importing pages
from AIPlanner.pages.signup import signup # Sign up page
from AIPlanner.pages.processing import processing # Processing page used in sign up page
from AIPlanner.pages.success import success # Success page shown after successful sign up
from AIPlanner.classes.database import * # Database
from AIPlanner.pages.userlist import userlist # Userlist debugging page

#to run test environment
#>cd AIPlanner
#>py -3 -m venv .venv
#>reflex run
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
        self.task_name = task_name
        if self.task_name.strip():
            self.show_error = False
    
    def set_task_description(self, task_description: str):
        self.task_description = task_description

    def set_priority(self, priority: str):
        self.priority = priority

    def set_date_time(self, date_time: str):
        self.date_time = date_time
    
    ...

def task_input_form():
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
            min_height="85vh",
        ),
        rx.logo(),
    )

app = rx.App()
app.add_page(index)
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