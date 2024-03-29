# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

def write_tasks():
    '''
    Writes the current tasks in task_list to tasks.txt
    '''
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))

def task_string(task: dict, **number):
    '''
    takes a user task entry and an optional task number and translates it into a readable string.

    Parameters:
    task (dict): the task entry.
    **t_num (int): the optional task number. 

    Returns:
    A readable string representing the task.
    '''
    t_num = number.get("t_num", None)
    disp_str = ""
    if t_num is not None:
        disp_str += f"Task Number: \t {t_num}\n"
    disp_str += f"Task: \t\t {task['title']}\n"
    disp_str += f"Assigned to: \t {task['username']}\n"
    disp_str += f"Date Assigned: \t {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
    disp_str += f"Due Date: \t {task['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
    disp_str += f"Task Description: \n {task['description']}\n"
    return disp_str


def reg_user():
    '''
    Register a new user
    '''
    while True:
        '''Add a new user to the user.txt file'''
        # - Request input of a new username
        print("-----------------------------------")
        new_username = input("New Username: ")

        # - Request input of a new password
        new_password = input("New Password: ")

        # - Request input of password confirmation.
        confirm_password = input("Confirm Password: ")

        if new_username in username_password:
                print("A user with that username already exists. Please input another username.")
                continue

        # - Check if the new password and confirmed password are the same.
        if new_password == confirm_password:
            
            # - If they are the same, add them to the user.txt file,
            print("New user added")
            username_password[new_username] = new_password
            
            with open("user.txt", "w") as out_file:
                user_data = []
                for k in username_password:
                    user_data.append(f"{k};{username_password[k]}")
                out_file.write("\n".join(user_data))
                break

        # - Otherwise you present a relevant message.
        else:
            print("Passwords do no match\\n")

def add_task():
    '''Allow a user to add a new task to task.txt file
        Prompt a user for the following: 
            - A username of the person whom the task is assigned to,
            - A title of a task,
            - A description of the task and 
            - the due date of the task.'''
    # Check input user exists
    print("-----------------------------------")
    while True:
        task_username = input("Name of person assigned to task: ")
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
        else:
            break
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    # Check due date of task input correctly
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break

        except ValueError:
            print("Invalid datetime format. Please use the format specified")


    # Then get the current date.
    curr_date = date.today()
    ''' Add the data to the file task.txt and
        Include 'No' to indicate if the task is complete.'''
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)
    write_tasks()
    print("Task successfully added.")
    

def view_all():
    '''Reads the task from task.txt file and prints to the console in the 
        format of Output 2 presented in the task pdf (i.e. includes spacing
        and labelling) 
    '''
    print("-----------------------------------")
    for t in task_list:
        print(task_string(t))
        

def view_mine():
    '''Reads the task from task.txt file and prints to the console in the 
        format of Output 2 presented in the task pdf (i.e. includes spacing
        and labelling)
    '''
    print("-----------------------------------")
    # Check if there's been a change
    changed = False
    t_num = 0
    current_tasks = []
    # Print tasks for current user
    for t in task_list:
        if  t['username'] == curr_user:
            current_tasks.append(t)
            t_num += 1
            disp_str = task_string(t, t_num=t_num)
            print(disp_str)
    # Check if the user wants to make a change to a task
    while True:
        print("Select a task to edit or mark as complete. Input -1 to exit.")
        selection = input()
        if selection == "-1":
            break
        if not selection.isdigit():
            print("Please enter a number.")
            continue
        selection = int(selection)
        # Check the selected task number exists
        if selection <= 0 or selection > len(current_tasks):
            print("Not a valid task number.")
            continue

        selected_task = current_tasks[selection - 1]
        print(f"Your selection:\n\n{task_string(selected_task, t_num=selection)}")

        while True:
            print("Select one:\n0: Edit the task\n1: Mark task as complete\n-1: Go back")
            edit_mark = input()
            edit = False
            match edit_mark:
                case "-1":
                    print("\n")        
                    break
                case "0":
                    edit = True
                case "1":
                    edit = False
                case _:
                    print("Not a valid selection.\n")
                    continue
            # Mark task as complete
            if not edit:
                selected_task["completed"] = True
                changed = True
                print(f"Task {selection} marked as complete.")
            # Edit task
            else:
                if selected_task["completed"]:
                    print(f"Task {selection} is already complete and cannot be edited. Please select another task.\n")
                    break
                while True:
                    print("Select one:\n0: Change the user to whom the task is assigned\n1: Change the task's due date\n-1: Go back")
                    name_date = input()
                    name = False
                    match name_date:
                        case "-1":
                            print("\n")
                            break
                        case "0":
                            name = True
                        case "1":
                            name = False
                        case _:
                            print("Not a valid selection.\n")
                            continue
                    # Edit who the task is assigned to
                    if name:
                        while True:
                            print("Enter user to assign task to.")
                            new_user = input()

                            if not new_user in username_password:
                                print("No user by that name exists.\n")
                                continue

                            selected_task["username"] = new_user
                            print(f"Task {selection} assigned to user {new_user}")
                            changed = True
                            break
                    # Edit the due date
                    else:
                        while True:
                            print("Enter the new due date in the format yyyy-mm-dd.")
                            new_date = input().split("-")
                            correct_format = True
                            for elem in new_date:
                                if not elem.isdigit():
                                    correct_format = False
                            if len(new_date) != 3 or not correct_format:
                                print("Invalid date format. Please enter the day, month, and year as numbers, separated by dashes (-)).\n")
                                continue
                            # Check the date is formatted correctly
                            try:
                                due_date = datetime(int(new_date[0]), int(new_date[1]), int(new_date[2]))
                                selected_task["due_date"] = due_date
                                changed = True
                                print(f"Task {selection} now due on {due_date.strftime(DATETIME_STRING_FORMAT)}.\n")
                                break

                            except ValueError:
                                print("Not a valid date.\n")
                                continue
    # Save changes
    if changed:
        print("Changes saved.\n")
        write_tasks()

def task_overview():
    '''
    Generates the task_overview and user_overview files based on the current task_list
    '''
    completed = 0
    overdue = 0
    user_tasks = {}
    # Generate user dictionary
    for u in username_password:
        user_tasks[u] = {"number": 0, "fraction": 0.00,
                         "complete": 0.00, "incomplete": 0.00,
                         "overdue": 0.00}
    # Iterate through tasks
    for t in task_list:
        user_entry = user_tasks[t["username"]]
        user_entry["number"] += 1

        if t["completed"]:
            completed += 1
            user_entry["complete"] += 1

        elif t["due_date"] < datetime.today():
            overdue += 1
            user_entry["overdue"] += 1

    tasks = len(task_list)
    # If there are no tasks, exit
    if tasks == 0:
        print("There are no tasks currently assigned. Reports not generated.\n")
        return
    
    # Format the user dictionary
    for entry in user_tasks.items():
        u = entry[1]
        u_complete = u["complete"]
        u_number = u["number"]
        u_incomplete = u_number - u_complete
        number_zero = u_number == 0
        u["fraction"] = u_number / tasks * 100
        u["complete"] = u_complete / u_number * 100 if not number_zero else 100
        u["incomplete"] = u_incomplete / u_number * 100 if not number_zero else 0
        u["overdue"] = u["overdue"] / u_number * 100 if not number_zero else 0

    incomplete = tasks - completed
    
    # Generate the task report string
    write_string = ""
    write_string += f"Total number of tasks: \t\t\t {tasks}\n"
    write_string += f"Completed tasks: \t\t\t {completed}\n"
    write_string += f"Incomplete tasks: \t\t\t {incomplete}\n"
    write_string += f"Overdue tasks: \t\t\t\t {overdue}\n"
    write_string += f"Percentage of incomplete tasks: \t {incomplete / tasks * 100}%\n"
    write_string += f"Percentage of overdue tasks: \t\t {overdue / tasks * 100}%\n"

    # Write to the report files
    with open("task_overview.txt", "w") as overview:
        overview.write(write_string)
    with open("user_overview.txt", "w") as overview:
        to_write = f"Total number of users: \t {len(username_password)}\n"
        to_write += f"Total number of tasks: \t {tasks}\n\n"

        for u in user_tasks.items():
            entry = u[1]
            user_string = ""
            user_string += f"User: {u[0]}\n"
            user_string += f"\tTasks: \t\t\t\t {entry["number"]}\n"
            user_string += f"\tPercentage of all tasks: \t {entry["fraction"]}%\n"
            user_string += f"\tPercentage tasks complete: \t {entry["complete"]}%\n"
            user_string += f"\tPercentage tasks incomplete: \t {entry["incomplete"]}%\n"
            user_string += f"\tPercentage tasks overdue: \t {entry["overdue"]}%\n\n"
            to_write += user_string
        overview.write(to_write)
    print("Reports generated.\n")

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)

#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    menu = input(f'''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my tasks
gr - Generate reports{"\nds - Display statistics" if curr_user == "admin" else ""}
e - Exit
''').lower()
    print()
    match menu:

        case 'r':
            reg_user()

        case 'a':
            add_task()

        case 'va':
            view_all()

        case 'vm':
            view_mine()
                
        case 'gr':
            task_overview()

        case 'ds': 
            '''If the user is an admin they can display statistics about number of users
                and tasks.'''
            if (curr_user == 'admin'):
                num_users = len(username_password.keys())
                num_tasks = len(task_list)

                print("-----------------------------------")
                if not os.path.exists("task_overview.txt") or not os.path.exists("user_overview.txt"):
                    task_overview()
                print("-----------------------------------")
                with open("task_overview.txt", "r") as overview:
                    for line in overview:
                        print(line)
                print("-----------------------------------")
                with open ("user_overview.txt", "r") as overview:
                    for line in overview:
                        print(line)
                print("-----------------------------------")
            else:
                print("You have made a wrong choice, Please Try again")

        case 'e':
            print('Goodbye!!!')
            exit()

        case _:
            print("You have made a wrong choice, Please Try again")
