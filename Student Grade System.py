__version__ = "v0.2.1"
__author__ = "Asher Morales"

import json
import statistics

# Load JSON file into list called data
def load_storage():
    """load_storage() will load the data from the json file"""
    try:
        with open("dataForProgram.json") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print("json file does not exist")   # If it doesn't exist
        return {}   # Create an empty dictionary


def main():
    """main() handles user input and is the primary landing page"""
    is_valid, admin_id, admin_username = administrator_checker(data)

    if not is_valid:
        print("Admin verification failed, goobye")
        return

    while True:
        print(f"Welcome {admin_username}!")
        main_action = input("What would you like to do for your students?\n"
                        "NEW - Open 'New' menu\n"
                        "VIEW - View record\n"
                        "AVERAGE - Compute average\n"
                        "SAVE - Save\n"
                        "EXIT - End program\n"
                        "Choice: "
                        ).upper().strip()
        if main_action == "NEW":
            main_action = input("What would you like to do?\n"
                "RECORD - Add new record\n"
                "COURSE - Add a new course to an existing record\n"
                "GRADE - Add new grade to an existing course\n").upper().strip()
            if main_action == "RECORD":
                new_record(data)
            elif main_action == "COURSE":
                new_course(data)
            elif main_action == "GRADE":
                new_grade(data)
            else:
                print("Invalid choice, try again")
        elif main_action == "VIEW":
            view_student(data)
        elif main_action == "AVERAGE":
            average_grade(data)
        elif main_action == "SAVE":
            with open("data.json", "w") as file:
                json.dump(data, file, indent=4)
            print("Data saved successfully!")
        elif main_action == "EXIT":
            print("Goodbye")
            break
        else:
            print(f"Invalid choice, try again")



def administrator_checker(data):
    """Handles administrator access to modify data"""
    check_attempts = 3
    while check_attempts != 0:
        admin_id = input("Enter administrator ID or 'BACK' to go back: ")

        if admin_id == "BACK":
            break
        if admin_id in data["ADMIN"]:  # Checks if id is in data.json
            admin_username = input("Please input administrator username: ")

            if admin_username !=  data["ADMIN"][admin_id]["name"]:
                check_attempts -= 1
                print(f"User does not exist. {check_attempts} admin log-in attempts left")
                continue
            elif admin_username == data["ADMIN"][admin_id]["name"]:
                admin_password = input(f"Input administrator password for {admin_username}: ")

                if admin_password != data ["ADMIN"][admin_id]["password"]:
                    check_attempts -= 1
                    print(f"Invalid password. {check_attempts} admin log-in attempts left")
                elif admin_password == data["ADMIN"][admin_id]["password"]:
                    return True, admin_id, admin_username
                else:
                    check_attempts -= 1
                    print(f"Invalid input. {check_attempts} admin log-in attempts left")

        if admin_id not in data["ADMIN"]:  # Runs if id is NOT in data.json
            check_attempts -= 1
            print(f"Admin details do not exist or match the system. {check_attempts} admin log-in attempts left")
    print("Max attempt reached, try again later.")
    return False, None, None



def verify_user(data):
    """Handles ID checking and a user verification system"""
    check_attempts = 3
    while check_attempts != 0:
        id_handler = input("Enter student ID or 'BACK' to go back: ").upper().strip()

        if id_handler == "BACK":
            return False, None, None
        if id_handler in data["student(s)"]:  # Checks if id is in data.json
            username_handler = input("Please input username: ")

            if username_handler != data["student(s)"][id_handler]["name"]:
                check_attempts -= 1
                print(f"User does not exist. {check_attempts} attempts left")
                continue
            elif username_handler == data["student(s)"][id_handler]["name"]:
                return True, id_handler, username_handler

        if id_handler not in data["student(s)"]:  # Runs if id is NOT in data.json
            nousername_handler = input("User does not exist, would you like to create a new user? Y/N: ").upper().strip()

            if nousername_handler == "Y":
                new_record(data)
            elif nousername_handler == "N":
                check_attempts -= 1
                print(f"User does not exist. {check_attempts} attempts left")
                continue
            else:
                check_attempts -= 1
                print(f"Invalid input. {check_attempts} attempts left")

    print("Max attempt reached, try again later.")
    return False, None, None



def new_record(data):
    """Handles new record creation for new students"""
    check_attempts = 3
    while check_attempts != 0:
        new_id = input("Enter new user ID or 'BACK' to go back: ").upper().strip()

        if new_id == "BACK":
            break

        if new_id in data:
            check_attempts -= 1
            print(f"ID already exists. {check_attempts} attempts left")
            continue
        elif new_id not in data:
            new_id_name = input("Enter new ID name: ")
            data.update({new_id: {
                "name": new_id_name,
                "course(s)": {},
                "status": ""}})
            print("Student record added!")
            break
        else:
            check_attempts -= 1
            print(f"Invalid input. {check_attempts} attempts left") 
            continue



def new_course(data):
    """Handles adding new courses to existing student records"""
    is_valid, student_id, student_username = verify_user(data)
    while True:
        if not is_valid:
            break

        course_exists = input("Name for new course or 'BACK' to go back: ").upper().strip()

        if course_exists == "BACK":
            return
        if course_exists in data["student(s)"][student_id]["course(s)"]:
            check_attempts -= 1
            print(f"Course already exists! {check_attempts} attempts left")
            continue
        elif course_exists not in data["student(s)"][student_id]["course(s)"]:
            data["student(s)"][student_id]["course(s)"][course_exists] = []
            continue
    return



def new_grade(data):
    """Handles adding new grades to existing student"""
    is_valid, student_id, student_username = verify_user(data)
    while True:
        if not is_valid:
            break
        
        course_exists = input("Enter course name or 'BACK' to go back: ").upper().strip()

        if course_exists == "BACK":
            return
        if course_exists in data["student(s)"][student_id]["course(s)"]:
            print(f"You're about to modify the grade for {course_exists}.\nContinue? Y/N: ")
            if input().upper().strip() == "Y":
                try:
                    new_grade = int(input(f"Enter new grade for {course_exists}: "))
                except:
                    print("Invalid input")
                else:
                    data["student(s)"][student_id]["course(s)"][course_exists] = [new_grade]
                    continue
            elif input().upper().strip() == "N":
                continue
        else:
            print(f"{course_exists} does not exist")
            continue
    return



def view_student(data):
    is_valid, student_id, student_username = verify_user(data)

    while True:
        if not is_valid:
            print("ID not valid")
            return
        
        print(f"{student_id}{student_username}: \n"
              f"Courses{" " * 10}| Grades")
        for courses in data["student(s)"][student_id]["course(s)"]:
            for grades in data["student(s)"][student_id]["course(s)"][courses]:
                print(f"{courses}{" " * (10 + len("courses") - len(courses))}| {grades}")
        break
    return



def average_grade(data):
    is_valid, student_id, student_username = verify_user(data)

    if not is_valid:
        print("ID not valid")
        return
    print(f"The average grade for {student_username} is:\n"
          f"{statistics.mean([grade for courses in data["student(s)"][student_id]["course(s)"] for grade in data["student(s)"][student_id]["course(s)"][courses]])}\n"
          f"This means {student_username} has {'passed' if statistics.mean([grade for courses in data["student(s)"][student_id]["course(s)"] for grade in data["student(s)"][student_id]["course(s)"][courses]]) > 75 else 'failed'}"
              )
    data["student(s)"][student_id]["status"] = "passed"
    return



# Call
with open("data.json", "r") as file:
    data = json.load(file)
main()
