import json
from json import JSONDecodeError
from pathlib import Path


class Task:
    default_completion_symbol = "[Completed]"
    current_completion_symbol = default_completion_symbol

    def __init__(self, task_name):
        self.task_name = task_name
        self.completion_status = False

    def complete_task(self):
        self.completion_status = True

    def incomplete_task(self):
        self.completion_status = False

    @classmethod
    def class_attributes_to_dict(cls):
        return {"current_completion_symbol": cls.current_completion_symbol}


    def task_to_dict(self):
        return {
            "task_name": self.task_name,
            "completion_status": self.completion_status
        }

    @classmethod
    def set_completion_symbol(cls, completion_symbol):
        cls.current_completion_symbol = completion_symbol

    @classmethod
    def reset_completion_symbol(cls):
        cls.current_completion_symbol = cls.default_completion_symbol

    @classmethod
    def change_completion_symbol(cls, new_symbol):
        if new_symbol == "default":
            cls.reset_completion_symbol()
            return f"completion symbol reset as {cls.default_completion_symbol}"
        else:
            cls.set_completion_symbol(new_symbol)
            return f"completion symbol set to {new_symbol}"



# blueprint for creating taskManager objects. The taskmanager had no instance specific attributes
# if we made multiple task manager objects, they would all share the same all_tasks list
# because all_tasks was a class variable/list
# since I wanted different all_tasks for each object, I had to make all_tasks[] an instance variable
class TaskManager:
    # this automatically runs and initializes the object (self) with an empty list all_tasks
    # we dont need to manually insert attributes to initialize an object with attributes (such as an empty list).
    def __init__(self):
        self.all_tasks = []

    def return_task_name(self, task_number):
        return self.all_tasks[task_number - 1].task_name

    def add_task(self, task_object):
        self.all_tasks.append(task_object) #add task object to list

    def complete_a_task(self, task_at_number_n):
        self.all_tasks[task_at_number_n - 1].complete_task()

    def incomplete_a_task(self, task_at_number_n):
        self.all_tasks[task_at_number_n - 1].incomplete_task()

    def delete_task(self, task):
        self.all_tasks.pop(task - 1)

    # know amount of indexes in task
    def index_length(self):
        indexes = len(self.all_tasks)
        return indexes

    def rearrange_task(self, choice_1, choice_2):
        x = self.all_tasks[choice_1 - 1]
        y = self.all_tasks[choice_2 - 1]
        self.all_tasks[choice_1 - 1] = y
        self.all_tasks[choice_2 - 1] = x

    def check_if_task_exists(self, task_number):
        valid_task_numbers = self.index_length()
        if task_number in range(1, valid_task_numbers + 1):
            return task_number
        else:
            return False


headers = "-"*50

# CLI METHOD: no logic, only printing.
def main_menu():
    print("[1] View all tasks") #
    print("[2] add task") #
    print("[3] complete task") #COMPLETES TASK AT THE INDEX -1 SHOWN IN VIEW ALL TASKS.
    print("[4] incomplete a task")
    print("[5] rearrange tasks") #this and complete task uses verify integer. so we return tasks to both so they can do what they want.
    print("[6] change completion symbol")
    print("[7] delete task")

# PRINT ALL TASKS: for each object in our task manager object's list, print them.
def view_all_tasks_main(task_manager):
    count = 1
    print(headers)
    print("All Tasks")
    print(headers)

    for task_object in task_manager.all_tasks:
        if not task_object.completion_status:
            print(f"{count}: {task_object.task_name}")
        else:
            print(f"{count}: {task_object.task_name} {Task.current_completion_symbol}")
        count += 1

    print()




def verify_string(verify_this_string):
    if verify_this_string == "q":
        return "q"
    else:
        return verify_this_string


def verify_integer(verify_this_int):
    if verify_this_int == "q":
        return "q"
    if verify_this_int.isdigit():
        return int(verify_this_int) #because the input was a string, so we must convert.
    else:
        return False

#This is Reusable CLI layer. verify integer works without it, check if task exists works without it.
def verify_integer_and_task(task_manager):
    while True:
        users_input = input("Enter a task number: ").strip().lower()
        check_this_int = verify_integer(users_input)

        if check_this_int == "q": #in main if returned value == q we exit program.
            return "q"
        if check_this_int is False:
            print("Invalid integer.")
            continue

        # if task is a valid integer we proceed here

        task_number = task_manager.check_if_task_exists(check_this_int)

        if not task_number:
            print("Invalid task.")
            continue
        else:
            return task_number



# -----------------------------------------------------------------------------------------------

def complete_task_main(task_manager):
    print(headers)
    print("Complete a Task")
    print(headers)
    complete_this_task = verify_integer_and_task(task_manager)

    if complete_this_task == "q":
        return

    task_manager.complete_a_task(complete_this_task)
    print(f"Task '{task_manager.return_task_name(complete_this_task)}' successfully completed....")




def incomplete_a_task_main(task_manager):
    print(headers)
    print("Reverse completion status")
    print(headers)
    incomplete_this_task = verify_integer_and_task(task_manager)

    if incomplete_this_task == "q":
        return

    task_manager.incomplete_a_task(incomplete_this_task)
    print(f"Task '{task_manager.return_task_name(incomplete_this_task)}' incomplete...")




def rearrange_tasks_main(task_manager):
    print(headers)
    print("Rearrange Tasks")
    print(headers)
    task_1 = verify_integer_and_task(task_manager)

    if task_1 == "q":
        return

    task_2 = verify_integer_and_task(task_manager)

    if task_2 == "q":
        return

    print(f"Tasks '{task_manager.return_task_name(task_1)}' & '{task_manager.return_task_name(task_2)}' successfully re-ordered.")
    task_manager.rearrange_task(task_1, task_2)





def add_a_task_main(task_manager):
    print(headers)
    print("Add a Task")
    print(headers)
    user_input = input("Enter new task: ").strip().lower()
    new_task = verify_string(user_input)

    if new_task == "q":
        return

    new_task_object = Task(new_task)
    task_manager.add_task(new_task_object)

    print(f"Task: '{new_task}' successfully added...")
    return



def change_completion_symbol_main():
    print(headers)
    print("Change Completion Symbol")
    print(headers)
    user_input = input("Enter new completion symbol: ").strip().lower()
    new_symbol = verify_string(user_input)

    if new_symbol == "q":
        return

    if user_input == "default":
        Task.reset_completion_symbol()
        print(f"Completion symbol reset to: {Task.default_completion_symbol}")
        return

    Task.change_completion_symbol(new_symbol)
    print(f"Completion symbol changed from: '{Task.default_completion_symbol}' to: '{new_symbol}'")
    return



def delete_a_task_main(task_manager):
    print(headers)
    print("Delete Task")
    print(headers)
    task_to_delete = verify_integer_and_task(task_manager)

    if task_to_delete == "q":
        return

    print(f"Deleted: '{task_manager.return_task_name(task_to_delete)}'")
    task_manager.delete_task(task_to_delete)
    return







#------------------------MAIN PROGRAM--------------------------
BASE_DIR = Path(__file__).resolve().parent
path_2 = BASE_DIR / "to_do_app.json"
path_3 = BASE_DIR / "comp_symbol.json"
manager = TaskManager()

try:
    with open(path_2, "r") as file:
        recreated_task_list = json.load(file)

    for task_dict in recreated_task_list:
        recreated_task_object = Task(task_dict["task_name"])
        if task_dict["completion_status"]: #if it's true.
            recreated_task_object.complete_task()

        manager.all_tasks.append(recreated_task_object)

except FileNotFoundError:
    pass
except JSONDecodeError:
    pass


try:
    with open(path_3, "r") as file:

        key_symbol_dict = json.load(file)
        Task.current_completion_symbol = key_symbol_dict["current_completion_symbol"]

except FileNotFoundError:
    pass
except JSONDecodeError:
    pass







while True:
    print("Enter 'q' at any stage to exit the program.\n")
    main_menu()
    print()
    user_input = input("Enter menu option: ").strip()
    print()
    menu_option = verify_integer(user_input)

    if menu_option == "q":
        print("Program exited.")
        break
    if menu_option is False:
        print("invalid integer.")
        continue

    if menu_option == 1:
        view_all_tasks_main(manager)
    elif menu_option == 2:
        add_a_task_main(manager)
    elif menu_option == 3:
        view_all_tasks_main(manager)
        print()
        complete_task_main(manager)
    elif menu_option == 4:
        view_all_tasks_main(manager)
        print()
        incomplete_a_task_main(manager)
    elif menu_option == 5:
        view_all_tasks_main(manager)
        print()
        rearrange_tasks_main(manager)
    elif menu_option == 6:
        change_completion_symbol_main()
    elif menu_option == 7:
        view_all_tasks_main(manager)
        print()
        delete_a_task_main(manager)
    else:
        print("Invalid menu option.")
        continue

    input("\n\npress any key to return to menu: ")



list_of_tasks = []

for task_object in manager.all_tasks:
    list_of_tasks.append(Task.task_to_dict(task_object))
    #print(list_of_tasks)

with open(path_2, "w") as file:
    json.dump(list_of_tasks, file, indent=2)


with open(path_3, "w") as file:
    json.dump(Task.class_attributes_to_dict(), file, indent=2)


