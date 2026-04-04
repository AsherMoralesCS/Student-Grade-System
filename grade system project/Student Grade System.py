import json

data = {}

# Load JSON file into list called data
def load_storage():
    try:
        with open("dataForProgram.json") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print("json file does not exist")   # If it doesn't exist
        return {}   # Create an empty dictionary


def main():
    while True:
        menu_action = input("What would you like to do?\n"
                        "NEWR - Add new record\n"
                        "NEWC - Add a new course to an existing record\n"
                        "NEWG - Add new grade to an existing course\n"
                        "VIEW - View record\n"
                        "AVERAGE - Compute average\n"
                        "SAVE - Save\n"
                        "EXIT - End program\n"
                        "Choice: "
                        ).upper().strip()
        main_action(menu_action)


def main_action(menu_action):
    while True:
        if menu_action == "NEW": new_user()
        else: pass


def id_checker(data):
    while True:
        student_id_input = input("Enter student ID: ")

        if student_id_input in data: return student_id_input
        if student_id_input not in data:
            noid_handler = input("User does not exist, would you like to create a new user? Y/N: ").upper().strip()
            if noid_handler == "YES":
                new_id = input("Enter new user ID: ")
                new_id_name = input("Enter new ID name: ")
                data.append(new_id{name_id_name})
                return new_id
            elif noid_handler == "NO": break
    pass


def new_user():
    pass