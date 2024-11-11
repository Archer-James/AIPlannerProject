"""Testing file and page for OpenAI integration. Must have OpenAI API key set as an environment variable OPENAI_API_KEY to use."""

import os
import re
import datetime
from openai import OpenAI
import reflex
from AIPlanner.classes.database import UserManagementState

class AIState(UserManagementState):
    """State that holds variables related to AI generation and functions that use those variables"""
    
    processed_output = ""

    def send_request(self):
        '''Function to send an OpenAI API request to generate task date/time/duration assignments, currently prints to console'''
        OpenAI.api_key = os.environ["OPENAI_API_KEY"]

        client = OpenAI()

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": """
                You are a bot that takes user tasks and assigns them to slots on a calendar.
                These tasks can have a priority level with (1) being the highest and (3) being the lowest. 
                Higher priority tasks should be assigned to blocks before lower priority tasks. Do not make any changes or return anything other than the following format for each task. 
                Do not include anything like "Here's the output" or "Let me know if you'd like any adjustments". 
                Do not include the word hours in the response. Give output in the format as follows: 


                task_id = Integer from prompt
                task_name = String from prompt
                assigned_block_date = Generated date within the next 14 days from 11/7/2024
                assigned_block_start_time = Generated time between 9am and 5pm to begin the task, in military time
                assigned_block_duration = How long the task should be worked on"""},
                {
                    "role": "user",
                    "content": """
                task_id = 1
                task_name = "work on computer science"
                priority_level = 1

                task_id = 2
                task_name = "work on biology"
                priority_level = 2
                """
                }
            ]
        )

        print(completion.choices[0].message)
        self.processed_output = completion.choices[0].message

    def process_output(self, completion):
        '''Processes the output of an OpenAI API call using regular expressions 
        and prints the string result to the console'''
        full_string = f"{completion.choices[0].message}"
        # Define a regular expression pattern to match the content section
        pattern = r"content='(.*?)'"

        # Extract the content using re.search
        match = re.search(pattern, full_string)

        # If a match is found, extract the content
        if match:
            content = match.group(1)
            print(content)

        # Define pattern to match key-value pairs (handles each key-value pair in a task)
        key_value_pattern = r'(\w+[\w_]*\w*) = ("[^"]*"|\d+|\d{1,2}/\d{1,2}/\d{4}|[A-Za-z\s:]+)'

        # Define a pattern to match the beginning of each task (starting with task_id)
        task_pattern = r"(task_id\s*=\s*\d+)"

        # Split the content into separate tasks using task_id
        task_blocks = re.split(task_pattern, content)

        # Initialize a list to store dictionaries for each task
        tasks = []

        # Process each task block
        for task_block in task_blocks:
            # Skip empty or non-task parts
            if not task_block.strip():
                continue

            # Find all key-value pairs in the task block
            matches = re.findall(key_value_pattern, task_block)

            # Initialize a dictionary for the current task
            task_dict = {}

            # Process each key-value pair
            for key, value in matches:
                # Convert numerical values (like task_id and assigned_block_duration) to integers
                if value.isdigit():  # If the value is a number, convert it to an integer
                    value = int(value)
                elif '/' in value:  # If it’s a date string
                    try:
                        # Parse the date and format it to MM/DD/YYYY
                        date_obj = datetime.datetime.strptime(value, "%m/%d/%Y")
                        value = date_obj.strftime("%m/%d/%Y")
                    except ValueError:
                        # If it doesn't match expected date format, keep it as-is
                        pass
                elif value.startswith('"') and value.endswith('"'):  # If it's a string enclosed in quotes
                    value = value[1:-1]  # Remove the quotes
                if key.startswith('n'):
                    key = key[1:len(key)]

                # Store the key-value pair in the task dictionary
                task_dict[key] = value

            # Add the task dictionary to the tasks list
            tasks.append(task_dict)

        # Output the list of task dictionaries
        for task in tasks:
            #print("Task:")
            for key, value in task.items():
                print(f'{key}: {value}')
            print()  # Add a blank line between tasks for clarity
        return tasks
    