# Megdalia Bromhal
# 30 Sept. 2024

# Importing necessary modules
import reflex as rx
from AIPlanner.classes.database import AddUser
from rxconfig import config
from datetime import date, time, timedelta

def signup(state=AddUser):
    # Signup page 
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Sign Up", size="9"),
            rx.input(placeholder="Username", value=state.username, on_change=state.set_username),
            rx.input(placeholder="Canvas Hash ID", type="number", value=state.canvas_hash_id, on_change=state.set_canvas_hash_id),
            rx.input(placeholder="Password", type="password", value=state.password, on_change=state.set_password),
            rx.button("Add User", on_click=lambda: state.add_user()),
            spacing="5",
            justify="center",
            min_height="85vh",
        )
    )