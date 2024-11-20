"""Page to connect user's Canvas account to system.
"""

from datetime import datetime # Used to grab assignment due date specifics
import requests
import reflex as rx
from AIPlanner.pages.login import LoginState


class CanvasConnectState(rx.State): # Like extending a class
    """
    Canvas connect state.
    Error handles input for manual tokens and transforms Canvas tasks to system task objects.

    Attributes:
    _api_token (str): the user's API token for Canvas.
    canvas_url (str): the Canvas Instance url used to grab assignments from Canvas account.
    is_submitting (bool): flag that tracks if the user has clicked "Enter" for the login form.
        Keeps the user from happy-clicking.
    """
    _api_token: str = ""
    canvas_url:str = 'https://uncw.instructure.com' # 'https://YOUR_CANVAS_INSTANCE_URL'
    is_submitting: bool = False


    def get_favorite_courses(self):
        """
        Gets favorited courses from Canvas with Canvas API.
        Includes all course info. We'll use the course's id in main to grab the assignments.
        Checks for pagination with Canvas API (sometimes the API doesn't return all courses bc data is too big).

        Returns:
        courses (list): Python list of courses.
        """
        courses = []

        # Grabbing only favorited courses
        url = f'{self.canvas_url}/api/v1/users/self/favorites/courses'
        while url:
            response = requests.get(url, headers=self.get_headers(), timeout=20)
            response.raise_for_status()
            courses.extend(response.json())
            # Check for pagination
            url = response.links.get('next', {}).get('url')
        return courses


    def get_assignments_for_course(self, course_id):
        """
        Iterates through Canvas course and returns all assignments.
        Makes sure that Canvas API isn't paginating results.

        Parameters:
        course_id (int): Canvas course id used to identify course.

        Returns:
        assignments (list): Python list of assignment dictionaries (each assignment is a dictionary).
        """

        assignments = [] # We can filter for upcoming assignments in main for better run time

        url = f'{self.canvas_url}/api/v1/courses/{course_id}/assignments'
        try:

            while url:
                response = requests.get(url, headers=self.get_headers(), timeout=20)
                response.raise_for_status()

                assignments.extend(response.json())

                # Check for pagination
                url = response.links.get('next', {}).get('url')

        except requests.exceptions.HTTPError as e:
            print(f"Error in getting course info for course id: {e}")

        #return upcoming_assignments
        return assignments


    def get_headers(self):
        """
        Retreives the headers required for making an API request,
        initializing the headers with stored API token.

        Returns:
        dict: A dictionary containing the 'Authorization' header with the Bearer token.
        """
        return {
            'Authorization': f'Bearer {self._api_token}'
        }


    def grab_tasks(self):
        """
        Method that calls other methods that check API token and grabs tasks from Canvas.

        Returns:
        assignment_list (list): list of each assignment from Canvas, which is a dictionary.
        """

        # Making sure api_token exists
        if self._api_token == "":
            return "No api token passed"

        # Setting what the date is now, to use to determine which assignments are current
        curr_date = datetime.now()

        courses = self.get_favorite_courses() # Grabbing all favorited canvas courses
        for course in courses:
            course_id = course['id']
            assignments = self.get_assignments_for_course(course_id)

            # Error handling course name
            try:
                print(f"Upcoming Assignments for course: {course['name']}")
            except KeyError:
                print("Error getting name of course...using Id instead")
                print(f"Upcoming Assignments for course id: {course['id']}")

            # Printing assignments for course
            for assignment in assignments:

                # Checking that due date isn't None (don't print these assignments)
                if assignment['due_at'] is not None:
                    due_date = datetime.strptime(assignment['due_at'], "%Y-%m-%dT%H:%M:%SZ")

                    # If assignment is upcoming, print it
                    if due_date >= curr_date:
                        print(f"- {assignment['name']} (Due: {assignment['due_at']})")

            print("\n")
        return "Success"


    def process_token(self, input_data:dict):
        """
        Takes manual token from input on Connect Canvas page,
        error handles input.
        If input is deemed valid, it's sent to <class that grabs tasks from Canvas>.
        Else, an erorr message is returned to the user so they can try again.

        Parameters:
        input_data (dict): input data (API key) from webpage UI.
        """
        # print(f"Type of input data: {type(input_data)}")
        # Getting the manual token from the data package from the input form
        self._api_token = input_data.get("manual_token")

        # Setting flag to true to take away submit button
        self.is_submitting = True
        yield

        # Setting flag as True so we check both the char's and if it's a valid Canvas token
        token_valid = True

        # Checking for invalid or potentially-sql-injection values
        invalid_chars = ["'", ";", "--", "<", ">", "%", "$", "^", "-", "[", "]", "=", "OR", "AND", "DROP TABLE", "@"]

        # Looping through invalid char's; if valid, strip whitespace and continue
        for char in invalid_chars:
            if char in self._api_token:

                # Invalid input: tell user to try again
                token_valid = False
                self.is_submitting = False
                yield rx.toast("Invalid token. Please try again.")

        # Stripping manual token of leading or trailing whitespace
        self._api_token = self._api_token.strip()
        print("Cleaned token entered", self._api_token)

        # Only runs if token doesn't have any invalid char's
        if token_valid:
            # Redirect the user to a processing page so they can't happy-click
            # Grab all favorited courses and upcoming assignments
            try:
                result = self.grab_tasks()
                print(result)

                # Send user back to home page upon successful connection
                print("Successful Canvas connection")
                self.is_submitting = False
                return rx.redirect("/")

            except requests.exceptions.HTTPError:
                token_valid = False
                self.is_submitting = False
                yield rx.toast("Invalid API token. Please try again.")


def manual_token_input() -> rx.Component:
    """
    Takes the manual token from user and assigns to variable for other classes to use.
    When the user submits, the information from the form is processed through CanvasConnect state.

    Returns:
    Reflex card object that holds the input for the user's API and a 'go back' button.
    """
    return rx.card(
        rx.form(
            rx.vstack(
                rx.input(
                    placeholder="Enter Canvas manual token",
                    name="manual_token",
                    required=True,
                ),
            ),
            rx.button(
                "Enter", 
                type="submit",
                disabled=CanvasConnectState.is_submitting,
            ),
            on_submit=CanvasConnectState.process_token
        ),
    )


@rx.page(route="/manualtokens_connect_page")
def manualtokens_connect_page():
    """
    Returns:
    Base page for where the user can enter their manual token to connect Canvas.
    Includes an input box for the manual token, error handling and input verification,
    a link to instructions on creating a manual token with Instructure, 
    and a Go Back button that takes the user to the home page.
    """
    return rx.container(
        rx.heading("Enter Canvas Manual Token", size="8"),

        # Have input & check input for errors
        manual_token_input(),

        rx.vstack(
            rx.hstack(
                rx.heading("Don't know how?"),
                rx.link(
                    rx.button("Instructions (opens link)"),
                    href="https://community.canvaslms.com/t5/Canvas-Basics-Guide/How-do-I-manage-API-access-tokens-in-my-user-account/ta-p/615312",
                    is_external=True,
                ),
            ),
            rx.link(
                rx.button("Go back"),
                href="/",
                is_external=False,
            ),
        ),
    )


def check_if_logged_in():
    """
    Checks if user is logged in.
    Technecly, checks if the username exists as a state (global) variable.

    Returns:
    True if username exists (user logged in), false otherwise.
    """
    return rx.cond(
        LoginState.username,
        True, # If username exists (logged in)
        False # Username doesn't exist (not logged in))
    )


def show_log_in_first():
    """
    Returns:
    Shows a log in button, a sign up button, or a continue button to the manual token enter page.
    User can choose which page they want to redirect to.
    """
    return rx.vstack(
        # Log in first button
        rx.link(
            rx.button("Log in first to save Canvas entries"),
            href="/login",
            is_external=False,
        ),
        rx.heading("--- Or ---"),
        # Sign up button
        rx.link(
            rx.button("Sign Up"),
            href="/signup",
            is_external=False,
        ),
        rx.heading("--- Or ---"),
        # Continue without account button
        rx.link(
            rx.button("Continue without account"),
            href="/manualtokens_connect_page",
            is_external=False,
        ),
        spacing="5",
        justify="center",
    )


@rx.page(route="/canvas_connect")
def canvas_connect() -> rx.Component:
    """
    Returns:
    Main function that returns the foundations for the Canvas_Connect page.
    Includes a button that takes user back to home page.
    """
    return rx.container(
        rx.heading("Connect your Canvas account!", size="8"),
        rx.vstack(
            rx.cond(
                check_if_logged_in(), # Checking if user is logged in
                manualtokens_connect_page(), # Take user to connect canvas if logged in
                show_log_in_first() # Show option to log in first if not logged in
            ),
            rx.link(
                rx.button("Go back"),
                href="/",
                is_external=False,
            ),
        ),
        width="100%",
        height="100vh",
        padding="2em",
        spacing="4",
        justify="center",
    )

# Eof
