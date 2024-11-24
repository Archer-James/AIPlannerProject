"""Page to connect user's Canvas account to system.
"""

from datetime import datetime, date, time, timedelta # Used to grab assignment due date specifics
import requests
import reflex as rx
from AIPlanner.pages.login import LoginState # Grabbing login credentials
# Importing UserManagementState so we can create tasks in the system
import AIPlanner.classes.database as database


class CanvasConnectState(rx.State): # Like extending a class
    """
    Canvas connect state.
    Error handles input for manual tokens and transforms Canvas tasks to system task objects.

    Attributes:
    _api_token (str): the user's API token for Canvas.
    canvas_url (str): the Canvas Instance url used to grab assignments from Canvas account.
    """
    _api_token: str = ""
    canvas_url:str = 'https://uncw.instructure.com' # 'https://YOUR_CANVAS_INSTANCE_URL'


    def get_favorite_courses(self):
        """
        Gets favorited courses from Canvas with Canvas API.
        Includes all course info. We'll use the course's id in main to grab the assignments.
        Checks for pagination with Canvas API (sometimes the API doesn't return all courses bc data is too big).

        Returns:
        courses (list): Python list of courses.
        """
        courses = []

        # url = f'{CANVAS_URL}/api/v1/courses' # Grabbing all current and past courses
        # Grabbing only favorited courses
        url = f'{self.canvas_url}/api/v1/users/self/favorites/courses'
        # url = f'{self.canvas_url}/api/v1/courses'
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

        # Making an empty array so we can transport the assignments into task objects later
        assignment_list = []

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
                        assignment_list.append(assignment)

            print("\n")
        #return "Success"
        return assignment_list


    # def convert_to_tasks(self, assign_list:list):
    #     """
    #     Converts a list of Canvas assignments to system Task objects.

    #     Parameters:
    #     assign_list (list): List of Canvas Assignments in dictionary form.

    #     """

    #     for assignment in assign_list:
    #         # print(f"Assignment: {assignment}")
    #         # print(f"Type of assignment: {type(assignment)}")
    #         # print(f"Due at: {assignment['due_at']}, type of due date: {type(assignment['due_at'])}")

    #         # Check for duplicates here

    #         # Converting Canvas due date to datetime and date so we can turn it into a Task object
    #         due_at = datetime.strptime(assignment['due_at'], "%Y-%m-%dT%H:%M:%SZ")

    #         # Sending Canvas task to database.py to become a system task object and added to database
    #         # Making the start date to one hour before it's due, duration 1 hour
    #         database.UserManagementState.manual_add_task(recur_freq=1,
    #                                             due_date=date(due_at.year, due_at.month, due_at.day),
    #                                             task_name=assignment['name'],
    #                                             description=assignment['description'],
    #                                             priority_lvl=3,
    #                                             block_date=date(due_at.year, due_at.month, due_at.day),
    #                                             block_start_time=time(due_at.hour - 1, due_at.minute),
    #                                             block_duration=timedelta(hours=1)
    #                                             )


    def process_token(self, input_data):
        """
        Takes manual token from input on Connect Canvas page,
        error handles input.
        If input is deemed valid, it's sent to <class that grabs tasks from Canvas>.
        Else, an erorr message is returned to the user so they can try again.

        Parameters:
        input_data (TYPE?): input data (API key) from webpage UI.
        """
        print(f"Type of input data: {type(input_data)}")
        # Getting the manual token from the data package from the input form
        self._api_token = input_data.get("manual_token")

        # Checking for invalid or potentially-sql-injection values
        invalid_chars = ["'", ";", "--", "<", ">", "%", "$", "^", "-", "[", "]", "=", "OR", "AND", "DROP TABLE", "@"]

        # Looping through invalid char's; if valid, strip whitespace and continue
        for char in invalid_chars:
            if char in self._api_token:

                # Invalid input: tell user to try again
                return rx.toast("Invalid manual token. Please try again.")

        # Stripping manual token of leading or trailing whitespace
        self._api_token = self._api_token.strip()
        print("Cleaned token entered", self._api_token)

        # Grab all favorited courses and upcoming assignments
        #try:
        assign_list = self.grab_tasks()
            #print(result)
            #print(type(result))

            #try:
                # Send assignments to task objects
                #self.convert_to_tasks(result)
        print("In try")
        #print(LoginState.user_id)
        # print(result)
        #converter = ConvertToTasks()
        #ConvertToTasks.convert_to_tasks(result)

        print("Before for loop")

        # Signed in as Mary - 6

        for assignment in assign_list:

            due_at = datetime.strptime(assignment['due_at'], "%Y-%m-%dT%H:%M:%SZ")
            # print(f"LoginState.user_id: {LoginState.user_id}")
            #print(f"")

            new_task = database.Task(
                recur_frequency=7,  # Example for recurring frequency
                due_date=date(due_at.year, due_at.month, due_at.day),
                is_deleted=False,
                task_name=assignment['name'],
                description="hello", #assignment['description'],
                task_id=100,  # Example for unique task_id
                priority_level={"Low": 1, "Medium": 2, "High": 3}["Low"],
                assigned_block_date=date(due_at.year, due_at.month, due_at.day),  # Set to today or another relevant date
                assigned_block_start_time=time(due_at.hour - 1, due_at.minute),  # Set a fixed start time (e.g., 2 PM)
                assigned_block_duration=timedelta(hours=1),  # Set your desired duration
                user_id=2 #LoginState.user_id # Referencing LoginState user_id attribute (to connect user to tasks)
            )
            with rx.session() as session:
                session.add(new_task)
                session.commit() 

        print("After convert class")

            # except TypeError as e:
            #     print(f"Error with converting Canvas tasks to task objects: {e}")
            #     return rx.toast("Error converting Canvas assignments to system tasks. Please try again.")

        # except requests.exceptions.HTTPError as e:
        #     print(f"Error with API Key: {e}")
        #     return rx.toast("Invalid API token. Please regenerate an unexpired API token and try again.")

        # Send user back to home page upon successful connection
        print("Successful Canvas connection")
        return rx.redirect("/")

class ConvertToTasks():
    def convert_to_tasks(self, assign_list):
        """
        Converts a list of Canvas assignments to system Task objects.

        Parameters:
        assign_list (list): List of Canvas Assignments in dictionary form.
        """
        print("Before for loop")

        # Signed in as Mary - 6

        for assignment in assign_list:

            due_at = datetime.strptime(assignment['due_at'], "%Y-%m-%dT%H:%M:%SZ")
            print(f"LoginState.user_id: {LoginState.user_id}")

            new_task = database.Task(
                recur_frequency=7,  # Example for recurring frequency
                due_date=date(due_at.year, due_at.month, due_at.day),
                is_deleted=False,
                task_name=assignment['name'],
                description=assignment['description'],
                task_id=100,  # Example for unique task_id
                priority_level={"Low": 1, "Medium": 2, "High": 3}["Low"],
                assigned_block_date=date(due_at.year, due_at.month, due_at.day),  # Set to today or another relevant date
                assigned_block_start_time=time(due_at.hour - 1, due_at.minute),  # Set a fixed start time (e.g., 2 PM)
                assigned_block_duration=timedelta(hours=1),  # Set your desired duration
                user_id=LoginState.user_id # Referencing LoginState user_id attribute (to connect user to tasks)
            )
            with rx.session() as session:
                session.add(new_task)
                session.commit()

            # print(f"Assignment: {assignment}")
            # print(f"Type of assignment: {type(assignment)}")
            # print(f"Due at: {assignment['due_at']}, type of due date: {type(assignment['due_at'])}")

            # Check for duplicates before adding as new task
            # Run get user tasks, then reference state.tasks
            # with rx.session() as session:
            #     task_already_in = session.exec(
            #         state.tasks.select().where(
            #             state.tasks.name == assignment['name'],
            #         ),
            #     ).first()

            # # If user found, allow log in
            # if task_already_in:
            #     print(f"Skipping task: {assignment['name']} because already in database...")
            #     continue # Skip this task

            # with rx.session() as session:
            #     if session.exec(
            #         select(Customer).where(Customer.email == self.current_user["email"])
            #     ).first():
            #         return rx.window_alert("User with this email already exists")

            # rx.foreach(
            #     state.tasks,
            #     lambda task: rx.text(
            #         f"Task Name: {task.task_name}, Due Date: {task.due_date}, "
            #         f"Description: {task.description}, Priority: {task.priority_level}, "
            #         f"Task ID: {task.task_id}, is_deleted: {task.is_deleted}"
            #     )

            # Converting Canvas due date to datetime and date so we can turn it into a Task object
            # due_at = datetime.strptime(assignment['due_at'], "%Y-%m-%dT%H:%M:%SZ")

            # # Sending Canvas task to database.py to become a system task object and added to database
            # # Making the start date to one hour before it's due, duration 1 hour
            # print(date(due_at.year, due_at.month, due_at.day))
            # print(database.UserManagementState.user_id)
            # database.manual_add_task(recur_freq=1,
            #                         due_date=date(due_at.year, due_at.month, due_at.day),
            #                         task_name=assignment['name'],
            #                         description=assignment['description'],
            #                         priority_lvl=1,
            #                         block_date=date(due_at.year, due_at.month, due_at.day),
            #                         block_start_time=time(due_at.hour - 1, due_at.minute),
            #                         block_duration=timedelta(hours=1),
            #                         user_id=database.UserManagementState.user_id
            #                     )
            print("good")
        database.UserManagementState.get_user_tasks(user_id=database.UserManagementState.user_id)
        print(database.UserManagementState.tasks)


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
            rx.button("Enter", type="submit"),
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
                is_external=False),
            rx.cond(LoginState.user_id,
                rx.text(f"LoginState.user_id: {LoginState.user_id}"),
                rx.text("LoginState.user_id doesn't exist"),
            ),
            rx.cond(database.UserManagementState.user_id,
                rx.text(f"database.UserManagementState.user_id: {database.UserManagementState.user_id}"),
                rx.text("database.UserManagementState.user_id doesn't exist"),
            ),
            # rx.cond(database.Task.user_id,
            #     rx.tIext(f"database.UserManagementState.user_id: {database.UserManagementState.user_id}"),
            #     rx.text("database.UserManagementState.user_id doesn't exist"),
            # ),
            # rx.cond(database.Task.user_id,
            #     rx.text(f"database.Task.user_id: {database.Task.user_id}"),
            #     rx.text("database.Task.user_id doesn't exist"),
            # ),
            # rx.cond(database.Task.user,
            #     rx.text(f"database.Task.user: {database.Task.user}"),
            #     rx.text("database.Task.user doesn't exist"),
            # ),
        ),
    )


def check_if_logged_in():
    """
    Checks if user is logged in.
    Technechally, checks if the username exists as a state (global) variable.

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
            # rx.link(
            #     rx.button("Go back"),
            #     href="/",
            #     is_external=False,
            # ),
        ),
        width="100%",
        height="100vh",
        padding="2em",
        spacing="4",
        justify="center",
    )

# Eof
