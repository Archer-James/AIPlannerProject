# using datetime package to get date, time, and duration
from datetime import date, time, timedelta

class Task:
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

    #initialize all of the attributes
    def __init__(self, recur_frequency: int, due_date: date, is_deleted: bool,
                 task_name: str, description: str, task_id: int, priority_level: int,
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

            # toString method for Task class
    def __str__(self):
        return (f"Task ID: {self.task_id}\n"
                f"Task Name: {self.task_name}\n"
                f"Description: {self.description}\n"
                f"Due Date: {self.due_date}\n"
                f"Is Deleted: {self.is_deleted}\n"
                f"Recur Frequency: {self.recur_frequency}\n"
                f"Priority Level: {self.priority_level}\n"
                f"Assigned Block Date: {self.assigned_block_date}\n"
                f"Assigned Block Start Time: {self.assigned_block_start_time}\n"
                f"Assigned Block Duration: {self.assigned_block_duration}\n")

exampleTask1 = Task(1, date(2024, 10, 1), False, "example task", "example object for task class, recurs daily", 1, 1, date(2024, 10, 2), time(10), timedelta(minutes=90))
exampleTask2 = Task(7, date(2024, 10, 4), False, "example task 2", "example object for task class, recurs weekly", 2, 2, date(2024, 10, 2), time(12), timedelta(minutes=90))
exampleTask3 = Task(0, date(2024, 10, 3), True, "example task 3", "example object for task class, deleted and non-recurring", 3, 1, date(2024, 10, 1), time(12), timedelta(minutes=60))
exampleTask4 = Task(0, date(2024, 10, 3), True, "example task 4", "example object for task class, deleted and non-recurring", 4, 1, date(2024, 9, 30), time(12), timedelta(minutes=60))
exampleTask5 = Task(0, date(2024, 10, 3), False, "example task 5", "example object for task class, non-recurring", 5, 3, date(2024, 10, 1), time(15), timedelta(minutes=30))
exampleTasks = [exampleTask1, exampleTask2, exampleTask3, exampleTask4, exampleTask5]
for i in range(len(exampleTasks)):
    print(exampleTasks[i])