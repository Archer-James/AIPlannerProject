import reflex as rx
from rxconfig import config
from datetime import date, time, timedelta

class User(rx.Model, table=True):
    username: str
    canvas_hash_id: int
    password: str

class Task(rx.Model, table=True):
    recur_frequency: int
    due_date: date
    is_deleted: bool
    task_name: str
    description: str
    task_id: int
    priority_level: int
    assigned_block_date: date
    assigned_block_start_time: time
    assigned_block_duration: timedelta

class QueryUser(rx.State):
    name: str
    users: list[User]

    def get_users(self):
        with rx.session() as session:
            self.users = session.exec(
                User.select().where(
                    User.username.contains(self.name)
                )
            ).all()