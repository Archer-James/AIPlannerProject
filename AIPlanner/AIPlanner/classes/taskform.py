import reflex as rx
from rxconfig import config

class TaskState(rx.State):
    """The state related to the task input form."""
    task_name: str = ""
    task_description: str = ""
    priority: str = "Medium"
    date_time: str = ""
    show_error: bool = False
    show_full_task_input: bool = False
    show_full_description_input: bool = False

    def apply_task(self):
        """Apply task logic, showing error if fields are missing."""
        if not self.task_name.strip():
            self.show_error = True
        else:
            self.show_error = False
            print(f"Task applied: {self.task_name, self.task_description, self.priority, self.date_time}")
            self.task_name = ""
            self.task_description = ""
            self.priority = "Medium"
            self.date_time = ""

    def toggle_full_task_input(self):
        """Toggles visibility of full task name input."""
        self.show_full_task_input = not self.show_full_task_input

    def toggle_full_description_input(self):
        """Toggles visibility of full description input."""
        self.show_full_description_input = not self.show_full_description_input

    def set_task_name(self, task_name: str):
        """Setter for task name."""
        self.task_name = task_name
        if self.task_name.strip():
            self.show_error = False

    def set_task_description(self, task_description: str):
        """Setter for task description."""
        self.task_description = task_description

    def set_priority(self, priority: str):
        """Setter for priority."""
        self.priority = priority

    def set_date_time(self, date_time: str):
        """Setter for date and time."""
        self.date_time = date_time


def task_input_form():
    """
    Task input form layout.
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
                        right="10px",
                        top="50%",
                        transform="translateY(-50%)",
                        border="none",
                        background="transparent",
                        cursor="pointer",
                        padding="0",
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
                        right="10px",
                        top="50%",
                        transform="translateY(-50%)",
                        border="none",
                        background="transparent",
                        cursor="pointer",
                        padding="0",
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
            # Expanded inputs and error message
            rx.cond(
                TaskState.show_full_task_input,
                rx.text_area(
                    placeholder="Full Task Name",
                    on_change=TaskState.set_task_name,
                    value=TaskState.task_name,
                    height="50px",
                    width="50%",
                )
            ),
            rx.cond(
                TaskState.show_full_description_input,
                rx.text_area(
                    placeholder="Full Description",
                    on_change=TaskState.set_task_description,
                    value=TaskState.task_description,
                    height="50px",
                    width="50%",
                )
            ),
            rx.cond(
                TaskState.show_error,
                rx.text("Task name is required", color="red", font_size="sm"),
            ),
            align_items="stretch",
        ),
        width="100%",
    )
