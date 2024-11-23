import reflex as rx
from AIPlanner.classes.database import Task
from AIPlanner.classes.database import UserManagementState
from AIPlanner.classes.database import LoginState
import datetime
import calendar

class daily_cal (rx.State):
    """
    Class to set the variables for the daily calendar

    Attributes:
    (str) selected_date: date to show on the page
    (list[Task]) tasks_for_day: tasks from the date
    (str) title: title of page
    """
    selected_date: str = ""
    tasks_for_day: list[Task] = []
    title: str = ""

    def set_date(self, year: str, month: str, day: str):
        """Sets the selected date using integer values for year, month, and day."""
        try:
            print(f"Setting date with year: {year}, month: {month}, day: {day}")  # Debug print

            # Ensure that year, month, and day are integers
            year = int(year)
            month = int(month)
            day = int(day)

            # Validate that the month is within the correct range
            if month < 1 or month > 12:
                raise ValueError(f"Invalid month: {month}. Month must be between 1 and 12.")

            # Validate that the day is within the correct range for the given month and year
            try:
                self.selected_date = datetime.date(year, month, day)
                print(f"Selected date set to: {self.selected_date}")
            except ValueError as e:
                raise ValueError(f"Invalid day for {month}/{year}: {e}")
            self.title = str(calendar.month_name[int(month)])+" "+str(day)
        except ValueError as e:
            print(f"Error setting date: {e}")

def daily() -> rx.Component:
    """
    Daily calendar component

    Returns:
    Prints daily calendar
    """
    return rx.container(
        # Top row for the "Home" button
        rx.flex(
            rx.link(
                rx.button("Home"),
                href="/",
                is_external=False,
            ),
        justify="flex-start",  # Align the button to the left
        width="100%",  # Full width for alignment
        ),
        # Main content below the "Home" button
        rx.flex(
            rx.vstack(
                # Title at the top
                rx.heading(f"Tasks for {daily_cal.title}", size="xlg"),
                # Tasks list
                rx.foreach(
                    UserManagementState.tasks,  # Iterate through all tasks
                    lambda task: rx.cond(
                        # Filter tasks where the due date matches the selected date
                        task.due_date == daily_cal.selected_date,
                        rx.text(
                            f"- {task.task_name}: {task.description}",
                            style={
                                "color": Task.get_priority_color(task),  # Dynamically set text color
                            },
                        ),
                        None,  # Otherwise, do not display anything
                    ),
                ),
            ),
            direction="column",  # Stack elements vertically
            align="center",  # Center elements horizontally
            justify="center",  # Center elements vertically
            width="100%",  # Full width
        ),
        width="100%",  # Full width of the container
        align="center",  # Align container to the center
        justify="center",  # Center content vertically
        padding="1rem",  # Optional: Add padding for spacing
    )