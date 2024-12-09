"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

# Importing pages
from AIPlanner.classes.database import * # Database
from AIPlanner.classes.taskform import task_input_form
from AIPlanner.pages.login import LoginState # Login State used to get the user's username
from AIPlanner.pages.signup import SignupState # Sign up state used to redirect the user to the signup page
from AIPlanner.classes.taskform import task_input_form
from AIPlanner.pages.login import LoginState # Login State used to get the user's username
from AIPlanner.pages.signup import SignupState # Sign up state used to redirect the user to the signup page
from AIPlanner.classes.todo_list import todo_component
from AIPlanner.classes.CreateCal import GenCalendar
from AIPlanner.classes.WeeklyCal import GenWeeklyCal
from AIPlanner.classes.cal_comps import weekly_component
from AIPlanner.classes.ai import AIState
from AIPlanner.classes.database import UserManagementState as state

@rx.page(on_load=[GenCalendar.init_calendar,GenWeeklyCal.init_week])
def weekly() -> rx.Component:
    """Reflex component for base index page
    Returns:
    Prints weekly page of website
    """
    # Welcome Page (Index)
    return rx.container(
        rx.color_mode.button(position="top-right"),
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
            rx.link(
                rx.button("Show Debug Options"),
                href="/userlist",
                is_external=False,
            ),
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
        rx.color_mode.button(position="top-right"),
        ), rx.container(
            rx.color_mode.button(position="top-right"),
            rx.vstack(
                rx.center(
                weekly_component(),
                todo_component(),
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
