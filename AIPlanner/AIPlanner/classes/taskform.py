import random
from datetime import date, time, timedelta, datetime
from AIPlanner.classes.database import *
import reflex as rx
from rxconfig import config
from AIPlanner.pages.login import LoginState

class TaskState(LoginState):
    """
    Represents the state related to the task input form.

    Attributes:
    task_name (str): The name of the task.
    task_description (str): A brief description of the task.
    priority (str): The priority of the task (default is "Medium").
    date_time (str): The date and time in MM/DD/YY format (default is today's date).
    user_id (int): The ID of the user associated with the task.
    show_error (bool): Whether to display an error message (default is False).
    show_full_task_input (bool): Whether to display the full task input form (default is False).
    show_full_description_input (bool): Whether to display the full description input form (default is False).
    """
    task_name: str = ""
    task_description: str = ""
    priority: str = "Medium"
    # Set date_time to today's date in MM/DD/YY format
    date_time: str = datetime.now().strftime("%m/%d/%y")
    user_id = int # No idea if this does something
    show_error: bool = False
    show_full_task_input: bool = False
    show_full_description_input: bool = False

    def apply_task(self):
        """
        Checks if the required fields are filled and applies the task to the database.

        Parameters:
        None

        Returns:
        None: A new task is added to the database, and the fields are reset upon successful completion.
        """
        if not self.task_name.strip():
            self.show_error = True
        else:
            self.show_error = False

            try:
                due_date = datetime.strptime(self.date_time, "%m/%d/%y").date()
            except ValueError:
                print("Invalid date format. Defaulting to today's date.")
                due_date = datetime.now().date()  # fallback to current date

            new_task = Task(
                recur_frequency=7,  # Example for recurring frequency
                due_date=due_date,
                is_deleted=False,
                task_name=self.task_name,
                description=self.task_description,
                task_id=random.randint(1, 1000000),  # Example for unique task_id
                priority_level={"Low": 1, "Medium": 2, "High": 3}[self.priority],
                assigned_block_date=date.today(),  # Set to today or another relevant date
                assigned_block_start_time=time(14, 0),  # Set a fixed start time (e.g., 2 PM)
                assigned_block_duration=timedelta(hours=1),  # Set your desired duration
                user_id=self.user_id  # Referencing LoginState user_id attribute (to connect user to tasks)
            )
            with rx.session() as session:
                session.add(new_task)
                session.commit()  # Save to the database

            print(f"Task applied: {self.task_name, self.task_description, self.priority, due_date}")

            # Reset fields after adding the task
            self.task_name = ""
            self.task_description = ""
            self.priority = "Medium"
            self.date_time = datetime.now().strftime("%m/%d/%y")

    def toggle_full_task_input(self):
        """
        Toggles the visibility of the full task name input field.

        Parameters:
        None

        Returns:
        None
        """
        self.show_full_task_input = not self.show_full_task_input
        if self.show_full_task_input:
            self.show_full_description_input = False

    def toggle_full_description_input(self):
        """
        Toggles the visibility of the full description input field.

        Parameters:
        None

        Returns:
        None
        """
        self.show_full_description_input = not self.show_full_description_input
        if self.show_full_description_input:
            self.show_full_task_input = False

    def set_task_name(self, task_name: str):
        """
        Sets the task name and updates the error visibility based on the input.

        Parameters:
        task_name (str): The name of the task to be set.

        Returns:
        None
        """
        self.task_name = task_name
        if self.task_name.strip():
            self.show_error = False

    def set_task_description(self, task_description: str):
        """
        Sets the task description.

        Parameters:
        task_description (str): The description of the task to be set.

        Returns:
        None
        """
        self.task_description = task_description

    def set_priority(self, priority: str):
        """
        Sets the priority level of the task.

        Parameters:
        priority (str): The priority level to be set (e.g., "Low", "Medium", "High").

        Returns:
        None
        """
        self.priority = priority

    def set_date_time(self, date_time: str):
        """
        Sets the date and time for the task.

        Parameters:
        date_time (str): The date and time to be set in MM/DD/YY format.

        Returns:
        None
        """
        self.date_time = date_time


def task_input_form():
    """
    Creates the layout for the task input form.

    The form includes:
    - Task name input with an optional dropdown for expanded text input.
    - Task description input with an optional dropdown for expanded text input.
    - A priority dropdown to select the task priority ("Low", "Medium", "High").
    - A date and time input for setting the task's due date and time.
    - An "Apply Task" button to submit the task.
    - Conditional error messages and expanded input areas based on user interactions.

    Parameters:
    None

    Returns:
    rx.box: A container with the task input form layout, including all components.
    """
    return rx.box(
        rx.vstack(
            rx.hstack(
                # Task name with dropdown arrow
                rx.box(
                    rx.input(
                        placeholder="Task Name",
                        on_change=TaskState.set_task_name,
                        value=TaskState.task_name,
                        flex=1,
                        width="150px",
                        padding_right="0px",
                    ),
                    rx.button(
                        "▼",
                        on_click=TaskState.toggle_full_task_input,
                        position="absolute",
                        right="0px",
                        top="50%",
                        transform="translateY(-50%)",
                        border="none",
                        background="dark pink",
                        cursor="pointer",
                        padding="0 8px",
                    ),
                    # Added conditional text area centered with Task Name box
                    rx.cond(
                        TaskState.show_full_task_input,
                        rx.text_area(
                            placeholder="Full Task Name",
                            on_change=TaskState.set_task_name,
                            value=TaskState.task_name,
                            height="50px",
                            width="200px",  # Set width to match Task Name input
                            position="absolute",  # Position relative to rx.box container
                            top="100%",           # Place directly below Task Name input
                            left="50%",             # Align horizontally with Task Name input
                            transform="translateX(-50%)",  # Center alignment
                        ),
                    ),
                    position="relative",
                    width="100%",
                    flex=1,
                ),
                # Task description
                rx.box(
                    rx.input(
                        placeholder="Task Description",
                        on_change=TaskState.set_task_description,
                        value=TaskState.task_description,
                        flex=1,
                        width="200px",
                    ),
                    rx.button(
                        "▼",
                        on_click=TaskState.toggle_full_description_input,
                        position="absolute",
                        right="0px",
                        top="50%",
                        transform="translateY(-50%)",
                        border="none",
                        background="dark pink",
                        cursor="pointer",
                        padding="0 8px",
                    ),
                    # Added conditional text area centered with Task Description box
                    rx.cond(
                        TaskState.show_full_description_input,
                        rx.text_area(
                            placeholder="Full Task Description",
                            on_change=TaskState.set_task_description,
                            value=TaskState.task_description,
                            height="100px",
                            width="300px",  # Set width to match Task Description input
                            position="absolute",  # Position relative to rx.box container
                            top="100%",           # Place directly below Task Description input
                            left="50%",             # Align horizontally with Task Description input
                            transform="translateX(-50%)",  # Center alignment
                        ),
                    ),
                    position="relative",
                    width="100%",
                    flex=1,
                ),
                # Priority
                rx.select(
                    ["Low", "Medium", "High"],
                    placeholder="Priority: Medium",
                    on_change=TaskState.set_priority,
                    value=TaskState.priority,
                    flex=1,
                ),
                # Date and time input
                rx.input(
                    placeholder="Set Date/Time",
                    type_="datetime-local",
                    on_change=TaskState.set_date_time,
                    value=TaskState.date_time,
                    flex=1,
                    width="200px",
                ),
                # Apply task button
                rx.button("Apply Task", on_click=TaskState.apply_task, flex=1),
                spacing="0px",
            ),
            # # Expanded inputs and error message
            # rx.cond(
            #     TaskState.show_full_task_input,
            #     rx.text_area(
            #         placeholder="Full Task Name",
            #         on_change=TaskState.set_task_name,
            #         value=TaskState.task_name,
            #         height="50px",
            #         width="50%",
            #     )
            # ),
            # rx.cond(
            #     TaskState.show_full_description_input,
            #     rx.text_area(
            #         placeholder="Full Task Description",
            #         on_change=TaskState.set_task_description,
            #         value=TaskState.task_description,
            #         height="150px",
            #         width="50%",
            #     )
            # ),
            rx.cond(
                TaskState.show_error,
                rx.text("Task name is required", color="red", font_size="sm"),
            ),
            align_items="stretch",
        ),
        width="100%",
    )
