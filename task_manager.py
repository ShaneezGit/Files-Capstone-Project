# =====importing libraries===========

# import os module for file related operations
# import datetime module

import os
import datetime

# file paths for user and task files

user_file_path = "user.txt"
task_file_path = "tasks.txt"

# ====Login Section====

# define a function called read_username_password to read users details from user.txt file
# initialize an empty list to store users' information
# open file in read mode
# iterate through each line in the file
# remove any whitespaces from the line using the strip function
# check if the line contains a comma
# split the line to get username and password using split function
# append to users list
# use try-except block to handle potential 'FileNotFoundError' or Exception
# return the list of users

def read_username_password(file_path):
    users = []
    try:
        with open(file_path, "r") as file:
            for line in file:
                line = line.strip()
                if "," in line:
                    username, password = line.split(", ", 1)
                    users.append({"username": username, "password": password})
                else:
                    print(f"\nInvalid line in the file: {line}.")
    except FileNotFoundError:
        print(f"\nFile '{file_path}' not found.")
    except Exception as e:
        print(f"\nAn error occurred while reading the file: {e}")
    return users

# define a function called user_login to handle user login
# obtain users' informatioon from 'user.txt' file
# request user input for username and password
# display message for successful login in
# check if user information match with a user in the list
# return the logged_in_username
# display message for invalid details

def user_login():
    users = read_username_password(user_file_path)
    while True:
        logged_in_username = input("\nEnter your username: ").strip()
        logged_in_password = input("Enter your password: ").strip()

        for user in users:
            if (
                user["username"] == logged_in_username
                and user["password"] == logged_in_password
            ):
                print("\nLogin successful!")
                return logged_in_username

        print("\nInvalid login details. Please try again.")

# define function called new_user to add a new user to the file
# open the file in append mode
# to add new user information to the file
# write user details to the file
# display successfuly registered message
# use try-except block to handle potential exception
# display error message if exception occurs
# perform user login by calling user_login function

def new_user(file_path, username, password):
    try:
        with open(file_path, "a") as file:
            file.write(f"{username}, {password}\n")
            print("\nUser successfully registered!")
    except Exception as e:
        print(f"\nAn error occurred while adding the user: {e}")

# define function called admin_menu
# open the task file in read mode
# interate through each line in the file
# increment the task for each line

def admin_menu():
    try:
        total_users = len(read_username_password(user_file_path))
    except Exception as e:
        print(f"\nError occurred while fetching user details: {e}")
        total_users = 0

    try:
        with open(task_file_path, "r") as file:
            total_tasks = sum(1 for line in file)
    except FileNotFoundError:
        print(f"\nFile '{task_file_path}' not found.")
        total_tasks = 0
    except Exception as e:
        print(f"\nError occurred while fetching task details: {e}")
        total_tasks = 0    
   
    print(f"\nTotal number of users: {total_users}")
    print(f'Total number of tasks: {total_tasks}')

print("\n** Welcome to Task Manager! **")

logged_in_username = user_login()

# while loop to display menu options
# check if user is  admin
# display admin menu if admin
# display other menu if not admin
# using loop, handle each menu option based on user input

while True:
    if logged_in_username == "admin":
        menu = input(
            """\nSelect one of the following options:
    \n\tr\t - \t register a user 
    \ta\t - \t add task 
    \tva\t - \t view all tasks  
    \tvm\t - \t view my tasks 
    \ts\t - \t statistics
    \te\t - \t exit 
    : """
        ).lower()
    else:
        menu = input(
            """\nSelect one of the following options:
    \n\tr\t - \t register a user 
    \ta\t - \t add task 
    \tva\t - \t view all tasks  
    \tvm\t - \t view my tasks 
    \te\t - \t exit 
    : """
        ).lower()

    # if user inputs 'r':
    # request user to input a new username and password
    # request user to confirm password
    # check if entered passwords match
    # if username exists, prompt user to chose a different username
    # add a new user and display 'successfuly registered' message

    if menu == "r":
        if logged_in_username == "admin":
            while True:
                users = read_username_password(user_file_path)
                new_username = input("\nEnter a new username: ")
                new_password = input("Enter a new password: ")
                confirm_password = input("Confirm the password: ")

                if new_password != confirm_password:
                    print("\nPasswords do not match. Please try again.")
                else:
                    username_exists = any(
                        user["username"] == new_username for user in users
                    )
                    if username_exists:
                        print(
                            "\nUsername already exists. Please choose a different username."
                        )
                    else:
                        new_user(user_file_path, new_username, new_password)
                        print("\nUser successfully registered!")
                        break
        else:
            print("\nSorry! Only 'admin' is allowed to register new users.")

    # if user inputs 'a':
    # request the user to input task details
    # get the current date using the import function
    # convert input due date to datetimme
    # format due date as "DD MM YYYY"
    # format task data
    # append task data to the 'task.txt' file
    # use try-except block to handle potential 'ValueError' for invalid date format

    elif menu == "a":
        task_username = input("\nEnter the username of the person whom the task is assigned: ")
        task_title = input("Enter the title of the task: ")
        task_description = input("Enter the description of the task: ")
        task_due_date = input("Enter the due date of the task (DD Mmm YYYY): ")

        try:
            input_due_date = datetime.datetime.strptime(task_due_date, "%d %b %Y")
            formatted_due_date_str = input_due_date.strftime("%d %b %Y")
            current_date_str = datetime.date.today().strftime("%d %b %Y")

            task_data = f"\n{task_username}, {task_title}, {task_description}, {formatted_due_date_str}, No, {current_date_str}\n"

            with open(task_file_path, "a") as file:
                file.write(task_data)
            print("\nTask added successfully!\n")

        except ValueError:
            print(f"\nInvalid date format! Please use DD Mmm YYYY (e.g., 26 Nov 2023) ")

    # if user inputs 'va' 
    # open file in read mode
    # iterate through each line in the file 
    # split the line into task details using ',' to seperate 
    # check if the number of task details is greater or equal to 6
    # display task details if valid
    # diplay error message if invalid

    elif menu == "va":
        with open(task_file_path, "r") as file:
            for line in file:
                task_details = line.strip().split(",")
                if len(task_details) >= 6:
                    print("\nTask Details: ")
                    print(f"\nUsername:        {task_details[0]}")
                    print(f"Title:          {task_details[1]}")
                    print(f"Description:    {task_details[2]}")
                    print(f"Due date:       {task_details[3]}")
                    print(f"Status:         {task_details[4]}")
                    print(f"Task date:      {task_details[5]}")
                else:
                    print("\nInvalid task details format")

    # if user inputs 'vm'
    # check if there is a logged-in username 
    # check if tasks are founf for the logged-in user
    # open the task file in read mode
    # iterate through each line in the file
    # get task details from the line by using split function
    # check if the task username matches logged-in username
    # if it matches, display task details
    # display message if no tasks were found for user
    # else request user for login

    elif menu == "vm":
        if logged_in_username:
            found_tasks = False

            with open(task_file_path, "r") as file:
                for line in file:
                    task_details = line.strip().split(",")
                    if task_details[0].strip() == logged_in_username:
                        print("\nTask Details: ")
                        print(f"\nTask username:       {task_details[0]}")
                        print(f"Task title:         {task_details[1]}")
                        print(f"Task description:   {task_details[2]}")
                        print(f"Task due date:      {task_details[3]}")
                        print(f"Task status:        {task_details[4]}")
                        print(f"Task date:          {task_details[5]}")
                        print()
                        found_tasks = True

            if not found_tasks:
                print("\nNo tasks found for this user.")
        else:
            print("\nPlease log in to view your tasks.")

    # if admin inputs 's'
    # call admin_menu function

    elif menu == "s":
        if logged_in_username == "admin":
            admin_menu()

    # exit the program when 'e' is chosen from the menu

    elif menu == "e":
        print("\n** Goodbye!!! **")
        exit()

    else:
        print("\nYou have entered an invalid input. Please try again.")