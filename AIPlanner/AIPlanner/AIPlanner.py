"""Home page of AIPlanner project.

"""

import reflex as rx
from rxconfig import config

# Importing pages
from AIPlanner.pages.signup import signup # Sign up page
from AIPlanner.pages.processing import processing # Processing page used in sign up page
from AIPlanner.pages.success import success # Success page shown after successful sign up
from AIPlanner.classes.database import * # Database
from AIPlanner.pages.userlist import userlist # Userlist debugging page
from AIPlanner.pages.login import login # Log in page for existing users
from AIPlanner.pages.login import LoginState # Login State used to get the user's username
from AIPlanner.pages.signup import SignupState # Sign up state used to redirect the user to the signup page
from AIPlanner.pages.canvas_connect import canvas_connect # Canvas connect page used to connect user's Canvas tasks


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

    show_full_input: bool = False

    # Need to connect this with database
    def apply_task(self):
        """
        Apply task button that will give errors if there are missing required fields
        Will also reset after successful apply
        """
        # if there is nothing in task name after removing white space, show an error
        if not self.task_name.strip():
            self.show_error = True
        else:
            # need to create a task object and put it in database. Need to figure out
            # can have task be added independently into database
            # show what tasks are in the list by using database.py and userlist.py 
            self.show_error = False
            print(f"Task applied: {self.task_name, self.task_description, self.priority, self.date_time}")
            self.task_name = ""
            self.task_description = ""
            self.priority = "Medium"
            self.date_time = ""
    
    def toggle_full_input(self):
        """Toggles the visibility of the full task name input."""
        self.show_full_input = not self.show_full_input



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


def task_input_form():
    """
    Task bar initializer with task name, task description, priority, set date/time, and apply button.
    """
    return rx.box(
        rx.vstack(
            # Task inputs arranged in a horizontal line
            rx.hstack(
                # Task name with integrated dropdown arrow in the same input box
                rx.box(
                    rx.input(
                        placeholder="Task Name",
                        on_change=State.set_task_name,
                        value=State.task_name,
                        flex=1,
                        padding_right="30px",  # Space for the dropdown arrow inside
                    ),
                    rx.button(
                        "▼",  # Dropdown arrow
                        on_click=State.toggle_full_input,
                        position="absolute",  # Positioned inside the input
                        right="10px",  # Align it to the right inside the input
                        top="50%",  # Vertically center the dropdown arrow
                        transform="translateY(-50%)",  # Fix centering
                        border="none",  # No border for the button
                        background="transparent",  # Transparent background
                        cursor="pointer",
                        padding="0",  # Remove padding
                    ),
                    position="relative",  # Make sure the dropdown stays inside the input box
                    width="100%",  # Full width for the task name input box
                    flex=1,  # Allow it to take up space in the hstack
                ),
                # Task description input
                rx.input(
                    placeholder="Task Description",
                    on_change=State.set_task_description,
                    value=State.task_description,
                    flex=1,
                ),
                # Priority dropdown
                rx.select(
                    ["Low", "Medium", "High"],
                    placeholder="Priority: Medium",
                    on_change=State.set_priority,
                    value=State.priority,
                    flex=1,
                ),
                # Date and time input
                rx.input(
                    placeholder="Set Date/Time",
                    type_="datetime-local",
                    on_change=State.set_date_time,
                    value=State.date_time,
                    flex=1,
                ),
                # Apply task button
                rx.button("Apply Task", on_click=State.apply_task, flex=1),
                spacing="10px",  # Add a bit of spacing between the elements
            ),
            # Conditionally show the larger input box when dropdown is clicked
            rx.cond(
                State.show_full_input,
                rx.text_area(
                    placeholder="Full Task Name",
                    on_change=State.set_task_name,
                    value=State.task_name,
                    height="100px",  # Larger height for expanded input
                    width="100%",    # Full width
                )
            ),
            # Error message
            rx.cond(
                State.show_error,
                rx.text("Task name is required", color="red", font_size="sm"),
            ),
            align_items="stretch",
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

        # User stack
        rx.hstack(
            rx.heading("AIPlanner: Your Productivity Assistant", size="7"),
            show_login_signup(), # rx condition that decides which buttons to show (login, signup, log out)
            rx.link( # Button that takes user to Canvas Connect page
                rx.button("Connect to Canvas"),
                href="/canvas_connect",
                is_external=False,
            ),
            spacing="5",
            justify="left",
            min_height="10vh",
        ),

        # Developer & Task stack
        rx.hstack(
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
    )


def show_login_signup():
    """
    Condition statement that decides whether the home page should display login and signup buttons
    or "Hello <username>!" and log out button.
    """
    return rx.cond(
                LoginState.username, # checking if exists
                rx.hstack( # If the user is logged in
                    rx.button("Log out", on_click=LoginState.logout),
                    rx.text(f"Hello {LoginState.username}!"),),
                rx.hstack( # If user is not logged in
                    rx.button("Log in!", on_click=LoginState.direct_to_login),
                    rx.button("Sign up!", on_click=SignupState.direct_to_signup),),
            )


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
app.add_page(signup) # Adding a signup page (as defined in pages.signup)
app.add_page(processing) # Adding processing page (used in sign up page)
app.add_page(success) # Adding success page (used in sign up page)
app.add_page(userlist) # Adding debugging user list page
# Adding a signup page, alternative, **Discuss in meeting**
#app.add_page(signup, on_load=UserManagementState.fetch_all_users)
app.add_page(login) # Login page 
app.add_page(canvas_connect) # Page user can connect Canvas tasks in


if __name__ == "__main__":
    app.run()
# Eof
