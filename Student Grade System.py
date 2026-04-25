__version__ = "v0.2.2"
__author__ = "Asher Morales"

import json
import statistics

# Load JSON file into list called data
def storage():
    """load_storage() will load the data from the json file"""
    try:
        with open("dataForProgram.json") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print("json file does not exist")   # If it doesn't exist
        return {}   # Create an empty dictionary



class Access:
    def __init__(self, data):
        self.data = data
        self.id = next(iter(data["ADMIN"]))
        self.user_id = data["student(s)"]

    def administrator_id(admin):
        return admin.id

    def administrator_name(admin):
        return admin.data["ADMIN"][admin.id]["name"]
    
    def administrator_password(admin):
        return admin.data["ADMIN"][admin.id]["password"]

    def student_id(student):
        return student.user_id

    def student_name(student):
        return student.data["student(s)"][student.id]["name"]

    def student_password(student):
        return student.data["student(s)"][student.id]["password"]

    def student_courses(self):
        student = Access()
        course_list = [course for course in student.student_name["course(s)"]]
        return course_list
    
    def student_grade(self):
        student = Access()
        grade_list = [grades for course in student.student_courses for grades in course]
        return grade_list


class Menu:
    def __init__(self, data):
        self.data = data
        self.new = DataManager()
        self.verify = Verifier()
        self.view = View()


    def main(self):
        """main() handles user input and is the primary landing page"""
        is_valid, admin_id, admin_username = self.verify.administrator(self.data)

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
                    self.new.student_record()
                elif main_action == "COURSE":
                    self.new.student_course()
                elif main_action == "GRADE":
                    self.new.student_grade()
                else:
                    print("Invalid choice, try again")
            elif main_action == "VIEW":
                self.view.student_grades()
            elif main_action == "AVERAGE":
                self.view.average_grade()
            elif main_action == "SAVE":
                with open("data.json", "w") as file:
                    json.dump(self.data, file, indent=4)
                print("Data saved successfully!")
            elif main_action == "EXIT":
                print("Goodbye")
                break
            else:
                print(f"Invalid choice, try again")



class Verifier():
    def __init__(self):
        self.new = DataManager()
        self.access = Access()


    def administrator(self):
        """Handles administrator access to modify data"""
        check_attempts = 3
        while check_attempts != 0:
            admin_id = input("Enter administrator ID or 'BACK' to go back: ")

            if admin_id == "BACK":
                break

            if admin_id in self.access.administrator_id():  # Checks if id is in data.json
                admin_username = input("Please input administrator username: ")

                if admin_username !=  self.access.administrator_name():
                    check_attempts -= 1
                    print(f"User does not exist. {check_attempts} admin log-in attempts left")
                    continue

                admin_password = input(f"Input administrator password for {admin_username}: ")

                if admin_password != self.access.administrator_password():
                        check_attempts -= 1
                        print(f"Invalid password. {check_attempts} admin log-in attempts left")
                else:
                        return True, admin_id, admin_username
            else:
                check_attempts -= 1
                print(f"Invalid input. {check_attempts} admin log-in attempts left")
        return False, None, None


    def user(self):
        """Handles ID checking and a user verification system"""
        record_creator = self.new.record(self)

        check_attempts = 3
        while check_attempts != 0:
            id_handler = input("Enter student ID or 'BACK' to go back: ").upper().strip()

            if id_handler == "BACK":
                return False, None, None
            if id_handler in self.access.student_id:  # Checks if id is in data.json
                username_handler = input("Please input username: ")

                if username_handler != self.access.student_name:
                    check_attempts -= 1
                    print(f"User does not exist. {check_attempts} attempts left")
                    continue
                elif username_handler == self.access.student_name:
                    return True, id_handler, username_handler

            if id_handler not in self.access.student_id:  # Runs if id is NOT in data.json
                nousername_handler = input("User does not exist, would you like to create a new user? Y/N: ").upper().strip()

                if nousername_handler == "Y":
                    self.new.student_record()
                elif nousername_handler == "N":
                    check_attempts -= 1
                    print(f"User does not exist. {check_attempts} attempts left")
                    continue
                else:
                    check_attempts -= 1
                    print(f"Invalid input. {check_attempts} attempts left")

        print("Max attempt reached, try again later.")
        return False, None, None



class DataManager:
    def __init__(self, data, verifier):
        self.data = data
        self.verify = Verifier()


    def student_record(self):
        """Handles new record creation for new students"""
        check_attempts = 3
        while check_attempts != 0:
            new_id = input("Enter new user ID or 'BACK' to go back: ").upper().strip()

            if new_id == "BACK":
                break

            if new_id in self.data:
                check_attempts -= 1
                print(f"ID already exists. {check_attempts} attempts left")
                continue
            elif new_id not in self.data:
                new_id_name = input("Enter new ID name: ")
                self.data.update({new_id: {
                    "name": new_id_name,
                    "course(s)": {},
                    "status": ""}})
                print("Student record added!")
                break
            else:
                check_attempts -= 1
                print(f"Invalid input. {check_attempts} attempts left") 
                continue



    def student_course(self):
        """Handles adding new courses to existing student records"""
        is_valid, student_id, student_username = self.verify.user(self.data)
        while True:
            if not is_valid:
                break

            course_exists = input("Name for new course or 'BACK' to go back: ").upper().strip()

            if course_exists == "BACK":
                return
            if course_exists in self.data["student(s)"][student_id]["course(s)"]:
                check_attempts -= 1
                print(f"Course already exists! {check_attempts} attempts left")
                continue
            elif course_exists not in self.data["student(s)"][student_id]["course(s)"]:
                self.data["student(s)"][student_id]["course(s)"][course_exists] = []
                continue
        return



    def student_grade(self):
        """Handles adding new grades to existing student"""
        is_valid, student_id, student_username = self.verify.user(self.data)
        while True:
            if not is_valid:
                break

            course_exists = input("Enter course name or 'BACK' to go back: ").upper().strip()

            if course_exists == "BACK":
                return
            if course_exists in self.data["student(s)"][student_id]["course(s)"]:
                print(f"You're about to modify the grade for {course_exists}.\nContinue? Y/N: ")
                if input().upper().strip() == "Y":
                    try:
                        grade = int(input(f"Enter new grade for {course_exists}: "))
                    except:
                        print("Invalid input")
                    else:
                        self.data["student(s)"][student_id]["course(s)"][course_exists] = [grade]
                        continue
                elif input().upper().strip() == "N":
                    continue
            else:
                print(f"{course_exists} does not exist")
                continue
        return


class View():
    def __init__(self):
        self.data = data
        self.verify = Verifier()

    def student_grades(self):
        is_valid, student_id, student_username = self.verify.user(self.data)

        while True:
            if not is_valid:
                print("ID not valid")
                return
            
            print(f"{student_id}{student_username}: \n"
                f"Courses{" " * 10}| Grades")
            for courses in self.data["student(s)"][student_id]["course(s)"]:
                for grades in self.data["student(s)"][student_id]["course(s)"][courses]:
                    print(f"{courses}{" " * (10 + len("courses") - len(courses))}| {grades}")
            break
        return



    def average_grade(self):
        is_valid, student_id, student_username = self.verify.user(self.data)

        if not is_valid:
            print("ID not valid")
            return
        print(f"The average grade for {student_username} is:\n"
            f"{statistics.mean([grade for courses in self.data["student(s)"][student_id]["course(s)"] for grade in data["student(s)"][student_id]["course(s)"][courses]])}\n"
            f"This means {student_username} has {'passed' if statistics.mean([grade for courses in data["student(s)"][student_id]["course(s)"] for grade in data["student(s)"][student_id]["course(s)"][courses]]) > 75 else 'failed'}"
                )
        self.data["student(s)"][student_id]["status"] = "passed"
        return


index = Menu()
# Call
with open("data.json", "r") as file:
    data = json.load(file)
index.main()
