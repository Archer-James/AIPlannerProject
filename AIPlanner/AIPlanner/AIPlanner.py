"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
# Importing pages
from AIPlanner.pages.signup import signup # Sign up page
from AIPlanner.pages.success import success # Success page shown after successful sign up
from AIPlanner.classes.database import * # Database
from AIPlanner.pages.userlist import userlist # Userlist debugging page
from AIPlanner.pages.login import login # Log in page for existing users
from AIPlanner.classes.taskform import task_input_form
from AIPlanner.pages.login import LoginState # Login State used to get the user's username
from AIPlanner.pages.signup import SignupState # Sign up state used to redirect the user to the signup page
from AIPlanner.pages.canvas_connect import canvas_connect # Canvas connect page used to connect user's Canvas tasks
from AIPlanner.classes. todo_list import todo_component
from AIPlanner.classes.ai import *
from AIPlanner.classes.database import UserManagementState as state
from AIPlanner.classes.CreateCal import GenCalendar
from AIPlanner.classes.WeeklyCal import GenWeeklyCal
from AIPlanner.classes.cal_comps import *
from AIPlanner.pages.weekly import weekly
from AIPlanner.classes.daily_cal import daily

class State(rx.State):
    """The app state."""


@rx.page(on_load=[GenCalendar.init_calendar,GenWeeklyCal.init_week])
def index() -> rx.Component:
    """Reflex component for base index page
    
    Returns:
    Prints the homepage
    """
    # Welcome Page (Index)
    return rx.container(
        rx.hstack(
            rx.heading("AIPlanner: Your Productivity Assistant", size="7"),
            #show_login_signup(), # rx condition that decides which 
            #buttons to show (login, signup, log out)
            rx.link( # Button that takes user to Canvas Connect page
                rx.button("Connect to Canvas"),
                href="/canvas_connect",
                is_external=False,
            ),
            show_login_signup(),
            spacing="5",
            justify="start",
            min_height="10vh",
        ),

        # Developer & Task stack
        rx.hstack(


            # rx.link(
            #     rx.button("Show Debug Options"),
            #     href="/userlist",
            #     is_external=False,
            # ),
            task_input_form(),
            spacing="5",
            justify="center",
            min_height="15vh", # Squishing it up a tad so we can see the giant text

        ),
        rx.hstack(
            rx.button("Generate AI Schedule", on_click=lambda: AIState.send_request(state.tasks)),
            rx.text(f"{AIState.messageText}"),
            spacing="5",
            justify="center",
            min_height="10vh",
        )
    ), rx.container(

        ), rx.container(
                rx.center(
                calendar_component(),
                todo_component(),
                style={
                "alignItems": "top",  # Ensure the calendar stays at the top
                "justifyContent": "flex-start",
            },
            ),

            padding="50px",
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
app.add_page(weekly)
app.add_page(daily)

# Megdalia Bromhal - 30 Sept. 2024
# Adding a signup page (as defined in pages.signup)
app.add_page(signup)
# Adding success page (used in sign up page)
app.add_page(success)
# Adding debugging user list page
app.add_page(userlist)

app.add_page(login) # Login page
app.add_page(canvas_connect) # Page user can connect Canvas tasks in



if __name__ == "__main__":
    app.run()
# Eof
