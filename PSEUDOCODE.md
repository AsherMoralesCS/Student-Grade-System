

         LOOP forever 
             DISPLAY "Enter Student ID or type BACK:"
             INPUT student_id_check
             CONVERT student_id_check to uppercase
             IF student_id_check == "BACK" THEN
                 RETURN None
             ENDIF
             IF must_exist == TRUE THEN
                 IF student_id_check exists in data THEN
                     RETURN student_id_check
                 ELSE
                     DISPLAY "ID does not exist."
                 ENDIF
             ELSE IF must_exist == FALSE THEN
                 RETURN student_id_check
             ENDIF
         END LOOP
     END FUNCTION



     FUNCTION addNewRecord(data)
         CALL id_verification(data, FALSE)
         STORE result in student_id_check
         IF student_id_check is None THEN
             RETURN
         ENDIF
         IF student_id_check exists in data THEN
             DISPLAY "ID already exists. Overwrite? YES/NO"
             INPUT confirmation
             CONVERT confirmation to uppercase
             IF confirmation is not "YES" THEN
                 RETURN
             ENDIF
         ENDIF
         DISPLAY "Enter Student Name:"
         INPUT student_name
         CREATE new dictionary entry:
             data[student_id_check] = {
                 "name": student_name,
                 "course(s)": empty dictionary,
                 "status": empty string
             }
         CALL saveStorage()
         DISPLAY "Record successfully saved."
     END FUNCTION



     FUNCTION addNewCourse(data)
         CALL id_verification(data, TRUE)
         STORE result in student_id_check
         IF student_id_check is None THEN
             RETURN
         ENDIF
         DISPLAY "Enter Course Name:"
         INPUT course_name
         IF course_name already exists in data[student_id_check]["course(s)"] THEN
             DISPLAY "Course already exists."
             RETURN
         ENDIF
         CREATE empty list for grades:
             data[student_id_check]["course(s)"][course_name] = empty list
         CALL saveStorage()
         DISPLAY "Course added."
     END FUNCTION



     FUNCTION addNewGrade(data)
         CALL id_verification(data, TRUE)
         STORE result in student_id_check
         IF student_id_check is None THEN
             RETURN
         ENDIF
         IF student has no courses THEN
             DISPLAY "No courses available."
             RETURN
         ENDIF
         DISPLAY all courses of student
         DISPLAY "Enter Course Name:"
         INPUT course_name
         IF course_name not in student's courses THEN
             DISPLAY "Course does not exist."
             RETURN
         ENDIF
         DISPLAY "Enter Grade:"
         INPUT grade
         CONVERT grade to number
         APPEND grade to
             data[student_id_check]["course(s)"][course_name]
         CALL saveStorage()
         DISPLAY "Grade added."
     END FUNCTION



     FUNCTION viewRecord(data)
         CALL id_verification(data, TRUE)
         STORE result in student_id_check
         IF student_id_check is None THEN
             RETURN
         ENDIF
         DISPLAY student name
         FOR each course in data[student_id_check]["course(s)"]
             DISPLAY course name
             IF grade list is not empty THEN
                 CALCULATE average of grades
                 DISPLAY grades
                 DISPLAY average
             ELSE
                 DISPLAY "No grades yet."
             ENDIF
         END FOR
     END FUNCTION



     FUNCTION computeAverage(data)
         CALL id_verification(data, TRUE)
         STORE result in student_id_check
         IF student_id_check is None THEN
             RETURN
         ENDIF
         SET total_sum = 0
         SET total_count = 0
         FOR each course in data[student_id_check]["course(s)"]
             FOR each grade in course grade list
                 ADD grade to total_sum
                 INCREMENT total_count
             END FOR
         END FOR
         IF total_count > 0 THEN
             SET general_average = total_sum / total_count
             DISPLAY general_average
         ELSE
             DISPLAY "No grades available."
         ENDIF
     END FUNCTION



     FUNCTION deleteRecord(data)
         CALL id_verification(data, TRUE)
         STORE result in student_id_check
         IF student_id_check is None THEN
             RETURN
         ENDIF
         DISPLAY "Are you sure? YES/NO"
         INPUT confirmation
         CONVERT confirmation to uppercase
         IF confirmation == "YES" THEN
             DELETE data[student_id_check]
             CALL saveStorage()
             DISPLAY "Record deleted."
         ELSE
             DISPLAY "Deletion cancelled."
         ENDIF
     END FUNCTION



     FUNCTION mainMenu()
         LOOP forever
             DISPLAY:
                 NEWR - Add New Record
                 NEWC - Add New Course
                 NEWG - Add New Grade
                 VIEW - View Record
                 AVE  - Compute Average
                 DEL  - Delete Record
                 EXIT - Exit Program
             INPUT menu_action
             CONVERT menu_action to uppercase
             IF menu_action == "NEWR" THEN
                 CALL addNewRecord(data)
             ELSE IF menu_action == "NEWC" THEN
                 CALL addNewCourse(data)
             ELSE IF menu_action == "NEWG" THEN
                 CALL addNewGrade(data)
             ELSE IF menu_action == "VIEW" THEN
                 CALL viewRecord(data)
             ELSE IF menu_action == "AVE" THEN
                 CALL computeAverage(data)
             ELSE IF menu_action == "DEL" THEN
                 CALL deleteRecord(data)
             ELSE IF menu_action == "EXIT" THEN
                 CALL saveStorage()
                 BREAK loop
             ELSE
                 DISPLAY "Invalid choice."
             ENDIF
         END LOOP
     END FUNCTION



     CALL loadStorage()
     CALL mainMenu()



 END PROGRAM