
import reflex as rx
from AIPlanner.classes.database import UserManagementState



def todo_component( state = UserManagementState) -> rx.Component:
    '''
    Creates a "Todos" component displaying an ordered list of tasks.

    Returns:
        Component: A Reflex vertical stack with a heading, divider, 
                and list of user tasks.
    '''
    return rx.vstack(
        rx.heading("To Do"),
        rx.divider(),
        rx.foreach(
            state.tasks,
            lambda task: rx.hstack(
                rx.vstack(
                    f"{task.task_name}, Due: {task.due_date}"
                ),
                rx.menu.root(
                    rx.menu.trigger(
                        rx.button("⋮", variant="soft")  # Three vertical dots button
                    ),
                    rx.menu.content(
                        rx.menu.item("Edit Name"),
                        rx.menu.item("Edit Description"),
                        rx.menu.separator(),
                        rx.menu.item("Delete Task", color="red"),
                    )
                )
            )
        )
    )