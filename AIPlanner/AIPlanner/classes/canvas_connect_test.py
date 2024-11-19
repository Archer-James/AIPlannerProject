"""Test script to make sure the process of grabbing Canvas assignments works
before integrating with AIPlanner application.

REQUIREMENTS:
pip install requests (must be in venv)
OR python3 -m pip install types-requests

Copilot AI helped generate this code.
"""

from datetime import datetime # Used to grab assignment due date specifics
import requests

# Replace with your Canvas API token and Canvas URL
API_TOKEN = 'YOUR_CANVAS_API_TOKEN'
CANVAS_URL = 'https://uncw.instructure.com' # 'https://YOUR_CANVAS_INSTANCE_URL'

# Set up the headers with your token
headers = {
    'Authorization': f'Bearer {API_TOKEN}'
}

# Setting what the date is now, to use to determine which assignments are current
curr_date = datetime.now()


def get_all_courses():
    """
    Gets all the courses from Canvas API.
    Includes all course info. We'll use the course's id in main to grab the assignments.
    Checks for pagination with Canvas API (sometimes the API doesn't return all courses bc data is too big).

    Returns:
    courses (list): Python list of courses
    """
    courses = []
    # url = f'{CANVAS_URL}/api/v1/courses' # Grabbing all current and past courses
    # Grabbing only favorited courses
    url = f'{CANVAS_URL}/api/v1/users/self/favorites/courses'
    while url:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        courses.extend(response.json())
        # Check for pagination
        url = response.links.get('next', {}).get('url')
    return courses


def get_assignments_for_course(course_id):
    """
    Iterates through Canvas course and returns all assignments.
    Makes sure that Canvas API isn't paginating results.

    Parameters:
    course_id (int): Canvas course id used to identify course.

    Returns:
    assignments (list): Python list of assignment dictionaries (each assignment is a dictionary).
    """

    #total_assignments = []
    #upcoming_assignments = []
    assignments = [] # We can filter for upcoming assignments in main for better run time

    url = f'{CANVAS_URL}/api/v1/courses/{course_id}/assignments'
    try:

        while url:
            response = requests.get(url, headers=headers, timeout=20)
            response.raise_for_status()

            #total_assignments.extend(response.json())
            assignments.extend(response.json())

            # Check for pagination
            url = response.links.get('next', {}).get('url')

    except requests.exceptions.HTTPError as e:
        print(f"Error in getting course info for course id: {e}")

    #for assignment in total_assignments:
        # if assignment['due_at'] is not None:
        #     due_date = datetime.strptime(assignment['due_at'], "%Y-%m-%dT%H:%M:%SZ")

        #     if due_date >= curr_date:
        #         upcoming_assignments.append(assignment)

    #return upcoming_assignments
    return assignments


def main():
    """
    Main function that handles calling the Canvas API and printing each assignment
    for each course on Canvas.
    Prints only upcoming assignments.
    """

    courses = get_all_courses()
    for course in courses:
        course_id = course['id']
        assignments = get_assignments_for_course(course_id)

        #print(assignments)
        #if len(assignments) > 0:

        # Error handling course name
        try:
            print(f"Upcoming Assignments for course: {course['name']}")
        except KeyError:
            print("Error getting name of course...using Id instead")
            print(f"Upcoming Assignments for course id: {course['id']}")

        # Printing assignments for course
        for assignment in assignments:

            # Checking that due date isn't None (don't print these assignments)
            if assignment['due_at'] is not None:
                due_date = datetime.strptime(assignment['due_at'], "%Y-%m-%dT%H:%M:%SZ")

                # If assignment is upcoming, print it
                if due_date >= curr_date:
                    print(f"- {assignment['name']} (Due: {assignment['due_at']})")

        print("\n")


if __name__ == "__main__":
    main()

# Eof
