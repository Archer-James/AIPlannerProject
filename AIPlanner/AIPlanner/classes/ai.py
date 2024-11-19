"""Testing file and page for OpenAI integration. Must have OpenAI API key set as an environment variable OPENAI_API_KEY to use."""

import os
import re
import datetime
import time
from openai import OpenAI
from AIPlanner.classes.database import UserManagementState

class AIState(UserManagementState):
    """State that holds variables related to AI generation and functions that use those variables
    
    Attributes:
    processed_output: String state variable to hold final output of processing
    """

    processed_output = ""

    def send_request(self, tasks):
        '''Function to send an OpenAI API request to generate task date/time/duration assignments, currently prints to console
        
        Returns:
        task_string: String that contains the result of processing the completion of the API request
        '''

        inputMessage = ""
        for task in tasks:
            print(task)
            if task['is_deleted'] is False:
                inputMessage = inputMessage + f"task_id = {task['id']}\ntask_name = '{task['task_name']}\npriority_level = {task['priority_level']}\ndue_date = {task['due_date']}\n\n"
                print(task['id'])
        
        if not tasks:
            return "No tasks available to generate a schedule. Please add some and try again."
        currentTime = time.ctime()

        OpenAI.api_key = os.environ["OPENAI_API_KEY"]

        client = OpenAI()

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"""
                You are a bot that takes user tasks and assigns them to slots on a calendar. Tasks can have a priority level with (1) being the highest and (3) being the lowest. 
                Higher priority tasks should be assigned to blocks before lower priority tasks. Do not make any changes or return anything other than the following format for each task. 
                Do not include anything like "Here's the output" or "Let me know if you'd like any adjustments". The current date is {currentTime}, only schedule tasks after this time.
                Do not include the word hours in the response. Give output in the format as follows:  
                task_id = Integer from prompt
                task_name = String from prompt
                assigned_block_date = Generated date before task due date
                assigned_block_start_time = Generated time between 9am and 5pm to begin the task, in military time
                assigned_block_duration = How long the task should be worked on"""},
                {
                    "role": "user",
                    "content": f"""
                {inputMessage}
                """
                }
            ]
        )

        print(completion.choices[0].message.content)
        self.processed_output = self.process_output(completion.choices[0].message.content)

    def process_output(self, content):
        '''Processes the output of an OpenAI API call using regular expressions 
        and prints the string result to the console
        
        Parameters:
        completion: String that contains the raw completion returned by the OpenAI API

        Returns:
        task_string: String that contains the processed completion resuts
        '''
        # Regular expression to extract task details
        regex = re.compile(
            r"task_id\s*=\s*(\d+)\s*"
            r"task_name\s*=\s*'([^']+?)\s*'"
            r"assigned_block_date\s*=\s*(\d{4}-\d{2}-\d{2})\s*"
            r"assigned_block_start_time\s*=\s*([\d:]+)\s*"
            r"assigned_block_duration\s*=\s*(\d+)",
            re.DOTALL
        )

        # Extract matches and build dictionaries
        matches = regex.findall(content)
        tasks = [
            {
                "task_id": int(match[0]),
                "task_name": match[1].strip().replace("'", ""),
                "assigned_block_date": match[2],
                "assigned_block_start_time": match[3],
                "assigned_block_duration": int(match[4]),
            }
            for match in matches
        ]
        task_string = ""
        for task in tasks:
            for key, value in task.items():
                task_string = task_string + f'{key}: {value}\n'
        #print(task_string)
        return task_string
    