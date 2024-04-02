# Capstone Project.
# Importing datetime format.
from datetime import datetime, date

# Importing user library.
credentials = {}

# Opening the user.txt file.
try:
    with open('user.txt', 'r') as file_1:
        for line_1 in file_1:
                username, password = line_1.strip().split(', ')
                credentials[username] = password
except FileNotFoundError as error:
    print('The file that you are trying to open does not exist.')
    print('Please find the correct files: user.txt and tasks.txt')
    print(error)  
    print('You will not be able to login.')
        
# Function to prompt user for username and password to check if they exist in the file.
while True:
        username = input('Please enter your username: ')
        password = input('Please enter your password: ')

        if username in credentials:
            if credentials[username] == password:
                print(f'\nLogin successful! Welcome {username}!')
                break
            else:
                print('Invalid password. Please try again.\n')
        else:
            print('Username not found. Please try again.\n')

# Defining lists to store the extracted information for tasks.txt.
tasks_file = {}
assigned_to_list = []
task_list = []
description_list = []
date_assigned_list = []
due_date_list = []
task_completed_list = []

# Opening the tasks.txt file and splitting at right index.
try:
    with open('tasks.txt', 'r') as file_2:
        for line_2 in file_2:
            split_task = line_2.strip().split(',')
            assigned_to_list.append(split_task[0].strip())
            task_list.append(split_task[1].strip())
            description_list.append(split_task[2].strip())
            date_assigned_list.append(split_task[3].strip())
            due_date_list.append(split_task[4].strip())
            task_completed_list.append(split_task[5].strip())
except FileNotFoundError as error_2:
    print('The file that you are trying to open does not exist.')
    print(error_2)  
            
# Defining menu function.
def options():
    print('\nPlease select one of the following options:')
    print('a = add task.')
    print('va = view all tasks.')
    print('vm = view my tasks.')
    # To make sure only the admin can see those 2 options.
    if is_admin(username):
        print('r = register user. (admin only)')
        print('ds = display statistics. (admin only)')
    print('e = exit.')


# Function to determine if the user is an admin or not.
def is_admin(username):
    return username == 'admin'


# Function to validate the date format in adding task menu.
def validate_date_format(date_text):
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False


# Menu Section where user picks an option.
print('When you are finished using the program, please use the exit option. (option e.) ')
choice = True
options()
while choice != 'e':
    choice = input('Please enter your choice: ').lower()
    
    if choice == 'r':
        # Making sure only the admin can use the register option.
        if is_admin(username):
            while True:
            # Asking and saving details for new user.
                register_user_name = input('\nYou have chosen to register a new user.\nPlease enter a new username: ')
                print(f'The username you have selected is {register_user_name}.')
                break
            while True:
                register_user_password = input('\nPlease enter a password: ')
                register_user_password_2 = input('Please confirm your password: ')
                if register_user_password_2 == register_user_password:
                    print('\nYou have successfully registered a new user!')
                    print(f'New user registered: {register_user_name}!')
                    credentials[register_user_name] = register_user_password
                    # Adding the new user to the user.txt file.
                    with open('user.txt', 'a') as file_1:
                        file_1.write(f'\n{register_user_name}, {register_user_password}')
                    break
                else:
                    print('The password you have re-entered does not match.')
            options()
            pass
        else:
            print('\nOnly admins can register a new user in the system.')
            options()
        
    elif choice == 'a':
        while True:
            # Asking and saving details for new added task.
            task_username = input('\nYou have chosen to add a task for a user. \nPlease enter the username of the person the task is assigned to: ')
            # Tasks can only be added to existing users.
            if task_username not in credentials:
                print("Invalid username. Please enter a registered username.")
                continue
            print(f'The username you have selected is: {task_username}.')
            task_title = input('\nPlease enter the title of the task: ')
            print(f'The title you have selected is: {task_title}.')
            task_description = input('\nPlease enter a description of the task: ')
            print(f'The description of the task is: {task_description}.')
            while True:
                # Asking user for due date until a valid format is entered.
                task_due_date = input('\nPlease enter a due date for the task in the following format: YYYY-MM-DD: ')
                if validate_date_format(task_due_date):
                    print(f'The due date for the task is: {task_due_date}.')
                    break
                else:
                    print("Invalid date format. Please enter the date in the format YYYY-MM-DD.")
            print(f'The due date for the task is: {task_due_date}.')
            task_date_assigned = date.today()
            print(f'\nThe task was assigned on: {task_date_assigned}.')
            # Adding the new task to the lists.
            assigned_to_list.append(task_username)
            task_list.append(task_title)
            description_list.append(task_description)
            date_assigned_list.append(str(task_date_assigned))
            due_date_list.append(task_due_date)
            task_completed_list.append('No') 
            # Appending the new task to the tasks.txt file.
            with open('tasks.txt', 'a') as tasks_file:
                tasks_file.write(f'\n{task_username}, {task_title}, {task_description}, {task_date_assigned}, {task_due_date}, No')
            break
        print(f'You have successfully added a task to: {task_username}!')
        options()
        
    elif choice == 'va':
        # Printing tasks of all users neatly.
        print('\nAll tasks for all users information: \n')
        for i in range(len(assigned_to_list)):
            print('User assigned to task:      ', assigned_to_list[i])
            print('Task title:                 ', task_list[i])
            print('Task description:           ', description_list[i])
            print('Date assigned:              ', date_assigned_list[i])
            print('Due Date:                   ', due_date_list[i])
            print('Task Completed:             ', task_completed_list[i])
            print()
        options()
        
    elif choice == 'vm':
    # Printing tasks of the logged in user neatly.
        logged_in_username = username
        # Flag to check if any tasks are assigned to the user.
        tasks_assigned = False
        print(f'\nTasks only assigned to you:  ({username})\n')
        for i in range(len(assigned_to_list)):
            if assigned_to_list[i] == logged_in_username:
                tasks_assigned = True
                print('Task title:                 ', task_list[i])
                print('Task description:           ', description_list[i])
                print('Date assigned:              ', date_assigned_list[i])
                print('Due Date:                   ', due_date_list[i])
                print('Task Completed:             ', task_completed_list[i])
                print()
        if not tasks_assigned:
            print('You currently have no tasks assigned to you.')
        options()
        
    elif choice == 'ds':
    # Option for admin only to view the statistics of total users and tasks.
        if is_admin(username):
            total_users = len(credentials)
            print('\nYou have chosen to see the statistics of all registered users and all current tasks: \n')
            print(f'Total number of users: {total_users}.')
            total_tasks = len(task_list)
            print(f'Total number of tasks: {total_tasks}.')
            options()
            pass
        else:
            print('\nOnly admins can view the statistics option.')
            options()
        
    elif choice == 'e':
    # Exit option.
        print('\nAll data has been saved.')
        print('Goodbye and have a great day!\n')
        
    else:
        print('\nYou have entered an invalid option. Please enter a valid option.')
        options()
