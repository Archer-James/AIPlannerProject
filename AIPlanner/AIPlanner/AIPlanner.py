"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from rxconfig import config

# Importing pages
from AIPlanner.pages.signup import signup # Sign up page
from AIPlanner.pages.processing import processing # Processing page used in sign up page
from AIPlanner.pages.success import success # Success page shown after successful sign up
from AIPlanner.classes.database import * # Database
from AIPlanner.pages.userlist import userlist # Userlist debugging page


from AIPlanner.pages.login import login # Log in page for existing users
from AIPlanner.classes.taskform import task_input_form
from AIPlanner.pages.login import LoginState # Login State used to get the user's username
from AIPlanner.pages.signup import SignupState # Sign up state used to redirect the user to the signup page
from AIPlanner.pages.canvas_connect import canvas_connect # Canvas connect page used to connect user's Canvas tasks




# from pages.signup import signup  # Sign up page

from AIPlanner.classes.CreateCal import GenCalendar
from AIPlanner.classes.WeeklyCal import GenWeeklyCal
from AIPlanner.classes.cal_comps import cal_comps
from AIPlanner.pages.weekly import weekly
# to run test environment
# >cd AIPlanner
# >py -3 -m venv .venv
# >reflex run
# open http://localhost:3000/


class State(rx.State):
    """The app state."""
    user_tasks: List[str] = ["1", "3"] #List[Task] = []

    #def set_user_task_list(self):
        #"""Initializing user task list"""
        #pass
        #self.user_tasks = get_user_tasks()
        #Have to get the session and user id

def get_item(item):
    """
    Creates a list item with the given text.

    Args:
        item (str): Text to display in the list item.

    Returns:
        Component: A Reflex list item with the specified text.
    """
    return rx.list.item(
        rx.text(item, font_size="1.25em"),
    )

def todo_component() -> rx.Component:
    '''
      Creates a "Todos" component displaying an ordered list of tasks.

    Returns:
        Component: A Reflex vertical stack with a heading, divider, 
                   and an ordered list of user tasks.
    '''
    return rx.vstack(
        rx.heading("Todos"),
        rx.divider(),
        rx.list.ordered(
            rx.foreach(
                State.user_tasks,
                get_item,
            ),
        ),
        padding="1em",
        border_radius="0.5em",
        shadow="lg", 
    )

@rx.page(on_load=[GenCalendar.init_calendar,GenWeeklyCal.init_week])
def index() -> rx.Component:
    """Reflex component for base index page"""
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
        )

        ), rx.container(
            rx.color_mode.button(position="top-right"),
            rx.vstack(
                rx.center(
                calendar_component(),
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
def calendar_component():
    """
    Calendar initializer and caller
    """
    return rx.vstack(
        # Navigation buttons for previous and next months
        rx.hstack(
            cal_comps.calendar_component(),
            margin_bottom="20px",
        ),
        padding="50px",
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


app.add_page(login) # Login page
app.add_page(canvas_connect) # Page user can connect Canvas tasks in



if __name__ == "__main__":
    app.run()
# Eof
