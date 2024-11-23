import reflex as rx
from AIPlanner.classes.database import UserManagementState
from AIPlanner.pages.login import LoginState
from AIPlanner.classes.database import Task

def todo_component( state = UserManagementState) -> rx.Component:
    '''
    Creates a "Todos" component displaying an ordered list of tasks.

    Returns:
    Prints heading and user tasks in a stack
    '''
    return rx.vstack(
        rx.hstack(
            rx.heading("To Do"),
            rx.button(rx.icon("refresh-ccw")
                      ,on_click = UserManagementState.get_user_tasks(LoginState.user_id)),
        ),
        rx.divider(),
        rx.foreach(
            state.tasks,
            lambda task: rx.hstack(
                rx.vstack(
                    f"{task.task_name}, Due: {task.due_date}",
                    style={
                                "color": 
                                Task.get_priority_color(task),
                            },
                ),
                rx.menu.root(
                    rx.menu.trigger(
                        rx.button("⋮", variant="soft")  # Three vertical dots button
                    ),
                    rx.menu.content(
                        rx.menu.item(
                            "Edit Name", 
                            on_click=lambda: state.edit_task_name(task.task_id)
                        ),
                        rx.menu.item(
                            "Edit Description", 
                            on_click=lambda: state.edit_task_description(task.task_id)
                        ),
                        rx.menu.separator(),
                        rx.menu.item(
                            "Delete Task", 
                            color="red",
                            on_click=lambda: state.delete_task(task.task_id)
                        ),
                    )
                )
            )
        )
    )
