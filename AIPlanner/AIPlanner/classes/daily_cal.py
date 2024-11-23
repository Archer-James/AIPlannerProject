import reflex as rx
from AIPlanner.classes.database import Task
from AIPlanner.classes.database import UserManagementState
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

    def set_date(self,month,year,day):
        """
        Sets the selected_date and title variables
        Parameters:
        month (int): integer number of month
        year(int): integer number of year
        day(int): integer number of day
        """
        self.selected_date = datetime.date(year,month,day)
        self.title = str(calendar.month_name[int(month)])+" "+str(day)

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
                rx.heading(f"Tasks for {daily_cal.title}", size="lg"),
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