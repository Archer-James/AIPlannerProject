"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from rxconfig import config
# from pages.signup import signup # Sign up page

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
            task_input_form(),
            spacing="5",
            justify="center",
            min_height="85vh",
        
        ),
        rx.logo(),
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
                href = "/",
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