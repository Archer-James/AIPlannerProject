from datetime import date, time, timedelta

class Task:
    recur_frequency: str
    due_date: date
    is_deleted: bool
    task_name: str
    description: str
    task_id: int
    priority_level: str
    assigned_block_date: date
    assigned_block_start_time: time
    assigned_block_duration: timedelta

    def __init__(self, recur_frequency: str, due_date: date, is_deleted: bool,
                 task_name: str, description: str, task_id: int, priority_level: str,
                 assigned_block_date: date, assigned_block_start_time: time, assigned_block_duration: timedelta):
        self.recur_frequency = recur_frequency
        self.due_date = due_date
        self.is_deleted = is_deleted
        self.task_name = task_name
        self.description = description
        self.task_id = task_id
        self.priority_level = priority_level
        self.assigned_block_date = assigned_block_date
        self.assigned_block_start_time = assigned_block_start_time
        self.assigned_block_duration = assigned_block_duration
