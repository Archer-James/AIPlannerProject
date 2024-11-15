'''
Creates a "Todos" component displaying an ordered list of tasks.

    Returns:
        Component: A Reflex vertical stack with a heading, divider, 
                and list of user tasks.
'''
import reflex as rx
from AIPlanner.classes.database import UserManagementState



def todo_component(state=UserManagementState) -> rx.Component:
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
                    f"{task.task_name}, Due: {task.due_date}",
                    f"Description: {task.description}"
                ),
                # Task Name Editing
                rx.cond(
                    state.editing_task_id_name == task.id,
                    rx.hstack(
                        rx.input(
                            value=state.new_task_name,  # Shows the current task name
                            on_change=lambda value: state.set_new_task_name(value),
                            width="200px",
                        ),
                        rx.button(
                            "Apply",
                            on_click=lambda: [
                                state.edit_task_name(task.id, state.new_task_name),
                                state.set_editing_task_id_name(None),  # Close the input box
                            ],
                        ),
                        rx.button(
                            "X",
                            on_click=lambda: state.set_editing_task_id_name(None),  # Revert to menu
                            color="black",
                        ),
                    ),
                    # Task Description Editing
                    rx.cond(
                        state.editing_task_id_description == task.id,
                        rx.hstack(
                            rx.input(
                                value=state.new_task_description,  # Shows the current description
                                on_change=lambda value: state.set_new_task_description(value),
                                width="300px",
                            ),
                            rx.button(
                                "Apply",
                                on_click=lambda: [
                                    state.edit_task_description(task.id, state.new_task_description),
                                    state.set_editing_task_id_description(None),  # Close the input box
                                ],
                            ),
                            rx.button(
                                "X",
                                on_click=lambda: state.set_editing_task_id_description(None),  # Revert to menu
                                color="black",
                            ),
                        ),
                        rx.menu.root(
                            rx.menu.trigger(
                                rx.button("⋮", variant="soft")  # Three vertical dots button
                            ),
                            rx.menu.content(
                                rx.menu.item(
                                    "Edit Name",
                                    on_click=lambda: [
                                        state.set_editing_task_id_name(task.id),
                                        state.set_new_task_name(task.task_name),  # Pre-fill with current name
                                    ],
                                ),
                                rx.menu.item(
                                    "Edit Description",
                                    on_click=lambda: [
                                        state.set_editing_task_id_description(task.id),
                                        state.set_new_task_description(task.description),  # Pre-fill with current description
                                    ],
                                ),
                                rx.menu.separator(),
                                rx.menu.item(
                                    "Delete Task",
                                    color="red",
                                    on_click=lambda: state.delete_task(task.id),
                                ),
                            ),
                        ),
                    ),
                )
            )
        ),
    )