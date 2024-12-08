import reflex as rx
from AIPlanner.classes.database import Task
from AIPlanner.classes.database import UserManagementState
import calendar
import datetime


class daily_cal(rx.State):
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
    month: int
    day: int

    def set_date(self, month: str, year: str, day: str):
        """Sets the selected date using integer values for year, month, and day."""
        year = int(year)
        month = int(month)
        self.month = month
        day = int(day)
        self.day = day
        self.selected_date = datetime.date(year, month, day)
        self.title = str(calendar.month_name[int(self.month)]) + " " + str(self.day)


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
                rx.button("Go Home"),
                href="/",
                is_external=False,
            ),
            justify="start",  # Align the button to the left
            width="100%",  # Full width for alignment
        ),
        # Main content below the "Home" button
        rx.flex(
            rx.heading(f"Tasks for {daily_cal.title}", size="6"),
            rx.vstack(
                # Tasks list
                rx.text("Tasks Due:"),
                rx.foreach(
                    UserManagementState.tasks,  # Iterate through all tasks
                    lambda task: rx.cond(
                        # Filter tasks where the due date matches the selected date
                        task.due_date == daily_cal.selected_date,
                        rx.text(
                            f"- {task.task_name}: {task.description}",
                            style={
                                "color":
                                Task.get_priority_color(task),
                                "wordWrap": "break-word",
                                "maxWidth": "800px",
                            },
                        ),
                        None,  # Otherwise, do not display anything
                    ),
                ),
                rx.text("Tasks assigned on this day:"),
                rx.foreach(
                    UserManagementState.tasks,  # Iterate through all tasks
                    lambda task: rx.cond(
                        # Filter tasks where the due date matches the selected date
                        task.assigned_block_date == daily_cal.selected_date,
                        rx.text(
                            f"- {task.task_name}: {task.description}"
                            f"<br>Assigned start time: {task.assigned_block_start_time}"
                            f"<br>Assigned block duration: {task.assigned_block_duration}",
                            style={
                                "color": Task.get_priority_color(task),
                                "wordWrap": "break-word",
                                "maxWidth": "800px",
                            },
                            dangerously_allow_html=True,  # Allows the use of HTML tags like <br>
                        ),
                        None,  # Otherwise, do not display anything
                    ),
                ),
            ),
            direction="column",  # Stack elements vertically
            align="center",  # Center elements horizontally
            justify="start",  # Align items to the top
            width="100%",  # Full width
        ),
        width="100%",  # Full width of the container
        align="center",  # Align container to the center
        justify="start",  # Align content to the top
        padding="1rem",  # Optional: Add padding for spacing
    )
