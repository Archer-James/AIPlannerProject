# """User class file

# Creates an instance of a User object with a username, password, and canvas_hash_id.
# Includes getters and setters, as well as an example list.

# """
# import csv


# #Adding comments for Sprint0 - Archer
# class User:
#     """A class that represents a user for the system."""
#     username: str
#     canvas_hash_id: int
#     password: str

#     def __init__(self, username: str, canvas_hash_id: int, password: str):
#         """Initializing user's characteristics."""
#         self.username = username
#         self.canvas_hash_id = canvas_hash_id
#         self.password = password

#     def describe_account(self):
#         """
#         Returns a string including the username, password, and canvas_hash_id of the user.
#         """
#         return f"{self.username}'s password is {self.password} and the canvas hash id is {self.canvas_hash_id}!"
#     def get_username(self):
#         """Returns the user's username."""
#         return self.username
#     def get_password(self):
#         """Returns the user's password."""
#         return self.password
#     def get_canvas_hash_id(self):
#         """Returns the user's canvas_hash_id."""
#         return self.canvas_hash_id
#     def set_username(self, username):
#         """Sets the user's username."""
#         self.username = username

#     def set_password(self, password):
#         """Sets the user's password."""
#         self.password = password

#     def set_canvas_hash_id(self, canvas_hash_id):
#         """Sets the user's canvas_hash_id."""
#         self.canvas_hash_id = canvas_hash_id

#     # Want to implement private setters and getters (not sure if access will be an issue then?)

# def create_user(username:str, canvas_hash_id:int, password:str):
#     """
#     Creates a new user with the User class and appends the user's info to a csv file.

#     param username: str         user's username
#     param canvas_hash_id: int   user's canvas id hashed
#     param password: str         user's password

#     returns new_user: User      new User object with username, canvas_hash_id, and password.
#     returns success_code: int   returns 0 if no error in appending the user to the csv, else 1.
#     """
#     new_user = User(username=username, canvas_hash_id=canvas_hash_id, password=password)
#     success_code = append_user_csv(new_user=new_user)

#     return new_user, success_code


# def append_user_csv(new_user: User):
#     """
#     Appends a new User object to a csv file acting as a database.

#     param new_user: User    the new user to be added to the database/csv

#     returns 0 if no error, 1 if error
#     """

#     try:
#         with open("AIPlanner/data/user_database.csv", mode='a', encoding="utf-8") as f:
#             writer = csv.writer(f)
#             writer.writerow([
#                 new_user.get_username(),
#                 new_user.get_canvas_hash_id(),
#                 new_user.get_password()
#                 ])

#             return 0
#     except (FileNotFoundError, PermissionError, csv.Error):
#         return 1


# EXAMPLE_USER = [
#     User("bobby", int('0156372'), "bobisawesome"),
#     User("henrythebeast", int('0883737372'), "yothisishenry")]


# def show_example_data():
#     """Takes data from hard-coded example database and prints data about each user."""
#     for user in EXAMPLE_USER:
#         print(User.describe_account(user))

# #Eof
