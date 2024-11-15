# """Class that takes the Canvas API manual token and grabs the upcoming tasks for each favorite class.
# """

# from datetime import datetime # Used to grab assignment due date specifics
# import requests
# import reflex as rx

# class ProcessCanvasToken(rx.State):
#     """
#     Class that processes Canvas Manual Token and returns upcoming assignments
#     for favorite courses.
#     """
#     api_token: str = ""
#     canvas_url:str = 'https://uncw.instructure.com' # 'https://YOUR_CANVAS_INSTANCE_URL'
#     headers = {
#     'Authorization': f'Bearer {api_token}'
#     }


#     def get_favorite_courses(self):
#         """
#         Gets favorited courses from Canvas with Canvas API.
#         Includes all course info. We'll use the course's id in main to grab the assignments.
#         Checks for pagination with Canvas API (sometimes the API doesn't return all courses bc data is too big).

#         return courses: Python list of courses
#         """
#         courses = []

#         # Grabbing only favorited courses
#         url = f'{self.canvas_url}/api/v1/users/self/favorites/courses'
#         while url:
#             response = requests.get(url, headers=self.headers, timeout=20)
#             response.raise_for_status()
#             courses.extend(response.json())
#             # Check for pagination
#             url = response.links.get('next', {}).get('url')
#         return courses


#     def get_assignments_for_course(self, course_id):
#         """
#         Iterates through Canvas course and returns all assignments.
#         Makes sure that Canvas API isn't paginating results.

#         param course_id: int, Canvas course id

#         returns assignments: Python list of assignments
#         """

#         assignments = [] # We can filter for upcoming assignments in main for better run time

#         url = f'{self.canvas_url}/api/v1/courses/{course_id}/assignments'
#         try:

#             while url:
#                 response = requests.get(url, headers=self.headers, timeout=20)
#                 response.raise_for_status()

#                 assignments.extend(response.json())

#                 # Check for pagination
#                 url = response.links.get('next', {}).get('url')

#         except requests.exceptions.HTTPError as e:
#             print(f"Error in getting course info for course id: {e}")

#         #return upcoming_assignments
#         return assignments


#     def grab_tasks(self, checked_api_token:str):
#         """
#         Main method for class.
#         Calls method that grab all favorite courses and
#         method that grabs all assignments for those courses.

#         Prints upcoming assignments in the terminal.
#         """
#         self.api_token = checked_api_token

#         print("In grab tasks")

#         # Making sure api_token exists
#         if self.api_token == "":
#             return "No api token passed"

#         # Setting what the date is now, to use to determine which assignments are current
#         curr_date = datetime.now()

#         courses = ProcessCanvasToken.get_favorite_courses(self) # Grabbing all favorited canvas courses
#         for course in courses:
#             course_id = course['id']
#             assignments = ProcessCanvasToken.get_assignments_for_course(self, course_id)

#             # Error handling course name
#             try:
#                 print(f"Upcoming Assignments for course: {course['name']}")
#             except KeyError:
#                 print("Error getting name of course...using Id instead")
#                 print(f"Upcoming Assignments for course id: {course['id']}")

#             # Printing assignments for course
#             for assignment in assignments:

#                 # Checking that due date isn't None (don't print these assignments)
#                 if assignment['due_at'] is not None:
#                     due_date = datetime.strptime(assignment['due_at'], "%Y-%m-%dT%H:%M:%SZ")

#                     # If assignment is upcoming, print it
#                     if due_date >= curr_date:
#                         print(f"- {assignment['name']} (Due: {assignment['due_at']})")

#             print("\n")

# # Eof
    