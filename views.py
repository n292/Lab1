# views.py
import csv
import os
import time
import statistics
from course import Course
from student import Student
from professor import Professor
from grade import build_grade_hash_table

def professor_view(user_email):
    prof = Professor.get_professor_by_email(user_email)
    if not prof:
        print("Professor record not found.")
        return
    if not prof.courses:
        print("No courses assigned to you.")
        return
    while True:
        print("\n=== Professor View ===")
        print("Your Courses:")
        for i, course in enumerate(prof.courses, 1):
            print(f"{i}. {course}")
        print(f"{len(prof.courses)+1}. Logout")
        choice = input("Select a course to view details or logout: ")
        try:
            choice_int = int(choice)
            if choice_int == len(prof.courses) + 1:
                print("Logging out.")
                break
            elif 1 <= choice_int <= len(prof.courses):
                selected_course = prof.courses[choice_int-1]
                professor_course_menu(selected_course)
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def professor_course_menu(course_id):
    while True:
        print(f"\n=== Professor Menu for Course {course_id} ===")
        print("1. View Course Info")
        print("2. View Students in Course")
        print("3. View Grade Report for Course")
        print("4. Back to Course Selection")
        choice = input("Enter your choice: ")
        if choice == "1":
            courses = Course.load_courses()
            course = next((c for c in courses if c.course_id == course_id), None)
            if course:
                print(f"Course ID: {course.course_id}, Name: {course.course_name}, Credits: {course.credits}, Description: {course.description}")
            else:
                print("Course record not found.")
        elif choice == "2":
            students = Student.load_students()
            course_students = [s for s in students if course_id in s.courses]
            if course_students:
                print(f"\n--- Students in Course {course_id} ---")
                for s in course_students:
                    idx = s.courses.index(course_id)
                    grade = s.grades[idx] if idx < len(s.grades) else "N/A"
                    mark = s.marks[idx] if idx < len(s.marks) else "N/A"
                    print(f"ID: {s.student_id}, Name: {s.first_name} {s.last_name}, Email: {s.email_address}, Grade: {grade}, Marks: {mark}")
            else:
                print("No students found for this course.")
        elif choice == "3":
            students = Student.load_students()
            course_students = [s for s in students if course_id in s.courses]
            if course_students:
                print(f"\n--- Grade Report for Course {course_id} ---")
                marks_list = []
                for s in course_students:
                    idx = s.courses.index(course_id)
                    grade = s.grades[idx] if idx < len(s.grades) else "N/A"
                    mark = s.marks[idx] if idx < len(s.marks) else "N/A"
                    print(f"{s.first_name} {s.last_name} - Grade: {grade}, Marks: {mark}")
                    if isinstance(mark, int):
                        marks_list.append(mark)
                if marks_list:
                    avg = sum(marks_list) / len(marks_list)
                    med = statistics.median(marks_list)
                    print(f"Average Marks: {avg:.2f}")
                    print(f"Median Marks: {med}")
                else:
                    print("No marks available for this course.")
            else:
                print("No students found for this course.")
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

def student_view(user_email):
    while True:
        print("\n=== Student View ===")
        print("1. View My Record")
        print("2. Update My Contact Info")
        print("3. Logout")
        choice = input("Enter your choice: ")
        if choice == "1":
            student = Student.get_student_by_email(user_email)
            if student:
                print("\n--- My Record ---")
                print(f"ID: {student.student_id}")
                print(f"Name: {student.first_name} {student.last_name}")
                print(f"Email: {student.email_address}")
                print("Courses and Grades:")
                for i, course in enumerate(student.courses):
                    grade = student.grades[i] if i < len(student.grades) else "N/A"
                    mark = student.marks[i] if i < len(student.marks) else "N/A"
                    print(f"  - {course}: Grade {grade}, Marks {mark}")
            else:
                print("Student record not found.")
        elif choice == "2":
            student = Student.get_student_by_email(user_email)
            if student:
                print("Enter new values (leave blank to keep current value):")
                new_first = input("Enter First Name: ")
                new_last = input("Enter Last Name: ")
                new_email = input("Enter Email: ")
                update_fields = {}
                if new_first: update_fields['first_name'] = new_first
                if new_last: update_fields['last_name'] = new_last
                if new_email: update_fields['email_address'] = new_email
                Student.update_student(student.student_id, **update_fields)
            else:
                print("Student record not found.")
        elif choice == "3":
            print("Logging out.")
            break
        else:
            print("Invalid choice. Please try again.")

def admin_view():
    while True:
        print("\n=== Admin View ===")
        print("1. Student Management")
        print("2. Course Management")
        print("3. Professor Management")
        print("4. Display Full Grade Report")
        print("5. Logout")
        choice = input("Enter your choice: ")
        if choice == "1":
            admin_student_menu()
        elif choice == "2":
            admin_course_menu()
        elif choice == "3":
            admin_professor_menu()
        elif choice == "4":
            display_grade_report_full()
        elif choice == "5":
            print("Logging out.")
            break
        else:
            print("Invalid choice. Please try again.")

def admin_student_menu():
    while True:
        print("\n--- Admin Student Management ---")
        print("1. Add Student")
        print("2. Delete Student")
        print("3. Update Student")
        print("4. Display All Students")
        print("5. Search Student by Name")
        print("6. Sort Students by Name")
        print("7. Back")
        choice = input("Enter your choice: ")
        if choice == "1":
            student_id = input("Enter Student ID: ")
            email = input("Enter Email: ")
            first_name = input("Enter First Name: ")
            last_name = input("Enter Last Name: ")
            courses = input("Enter Courses (comma-separated): ")
            grades = input("Enter Grades (comma-separated, matching courses): ")
            marks = input("Enter Marks (comma-separated, matching courses): ")
            Student.add_student(Student(student_id, email, first_name, last_name, courses, grades, marks))
        elif choice == "2":
            student_id = input("Enter Student ID to delete: ")
            Student.delete_student(student_id)
        elif choice == "3":
            student_id = input("Enter Student ID to update: ")
            print("Enter new values (leave blank to keep current value):")
            first_name = input("Enter First Name: ")
            last_name = input("Enter Last Name: ")
            email = input("Enter Email: ")
            courses = input("Enter Courses (comma-separated): ")
            grades = input("Enter Grades (comma-separated): ")
            marks = input("Enter Marks (comma-separated): ")
            update_fields = {}
            if first_name: update_fields['first_name'] = first_name
            if last_name: update_fields['last_name'] = last_name
            if email: update_fields['email_address'] = email
            if courses: update_fields['courses'] = courses
            if grades: update_fields['grades'] = grades
            if marks: update_fields['marks'] = marks
            Student.update_student(student_id, **update_fields)
        elif choice == "4":
            Student.display_students()
        elif choice == "5":
            name = input("Enter name to search: ")
            Student.search_student_by_name(name)
        elif choice == "6":
            Student.sort_students_by_name()
        elif choice == "7":
            break
        else:
            print("Invalid choice. Please try again.")

def admin_course_menu():
    while True:
        print("\n--- Admin Course Management ---")
        print("1. Add Course")
        print("2. Delete Course")
        print("3. Update Course")
        print("4. Display Courses")
        print("5. Back")
        choice = input("Enter your choice: ")
        if choice == "1":
            course_id = input("Enter Course ID: ")
            course_name = input("Enter Course Name: ")
            credits = input("Enter Credits: ")
            description = input("Enter Description: ")
            Course.add_course(Course(course_id, course_name, credits, description))
        elif choice == "2":
            course_id = input("Enter Course ID to delete: ")
            Course.delete_course(course_id)
        elif choice == "3":
            course_id = input("Enter Course ID to update: ")
            print("Enter new values (leave blank to keep current value):")
            course_name = input("Enter Course Name: ")
            credits = input("Enter Credits: ")
            description = input("Enter Description: ")
            update_fields = {}
            if course_name: update_fields['course_name'] = course_name
            if credits: update_fields['credits'] = credits
            if description: update_fields['description'] = description
            Course.update_course(course_id, **update_fields)
        elif choice == "4":
            Course.display_courses()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")

def admin_professor_menu():
    while True:
        print("\n--- Admin Professor Management ---")
        print("1. Add Professor")
        print("2. Delete Professor")
        print("3. Update Professor")
        print("4. Display Professors")
        print("5. Back")
        choice = input("Enter your choice: ")
        if choice == "1":
            professor_id = input("Enter Professor ID: ")
            name = input("Enter Name: ")
            email = input("Enter Email: ")
            rank = input("Enter Rank: ")
            courses = input("Enter Courses (comma-separated): ")
            Professor.add_professor(Professor(professor_id, name, email, rank, courses))
        elif choice == "2":
            professor_id = input("Enter Professor ID to delete: ")
            Professor.delete_professor(professor_id)
        elif choice == "3":
            professor_id = input("Enter Professor ID to update: ")
            print("Enter new values (leave blank to keep current value):")
            name = input("Enter Name: ")
            email = input("Enter Email: ")
            rank = input("Enter Rank: ")
            courses = input("Enter Courses (comma-separated): ")
            update_fields = {}
            if name: update_fields['name'] = name
            if email: update_fields['email'] = email
            if rank: update_fields['rank'] = rank
            if courses: update_fields['courses'] = courses
            Professor.update_professor(professor_id, **update_fields)
        elif choice == "4":
            Professor.display_professors()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")

def display_grade_report_full():
    students = Student.load_students()
    if not students:
        print("No student records found.")
        return
    course_groups = {}
    for student in students:
        for idx, course in enumerate(student.courses):
            course_groups.setdefault(course, []).append((student, idx))
    for course_id, student_tuples in course_groups.items():
        print(f"\n--- Grade Report for Course {course_id} ---")
        marks_list = []
        for student, idx in student_tuples:
            grade = student.grades[idx] if idx < len(student.grades) else "N/A"
            mark = student.marks[idx] if idx < len(student.marks) else "N/A"
            print(f"{student.first_name} {student.last_name} - Grade: {grade}, Marks: {mark}")
            if isinstance(mark, int):
                marks_list.append(mark)
        if marks_list:
            avg = sum(marks_list) / len(marks_list)
            med = statistics.median(marks_list)
            print(f"Average Marks: {avg:.2f}")
            print(f"Median Marks: {med}")
        else:
            print("No marks available for this course.")

def main():
    print("=== Welcome to CheckMyGrade Application ===")
    print("1. Login")
    print("2. Register")
    choice = input("Enter your choice: ")
    if choice == "1":
        email = input("Enter email: ")
        password = input("Enter password: ")
        from login import LoginUser  # Local import if needed
        if not LoginUser.login(email, password):
            print("Invalid login credentials. Exiting.")
            return
        print("Login successful!")
    elif choice == "2":
        email = input("Enter email for registration: ")
        password = input("Enter password: ")
        role = input("Enter role (admin/professor/student): ").lower()
        from login import LoginUser  # Local import if needed
        new_user = LoginUser(email, password, role)
        LoginUser.register_user(new_user)
        print("Please login now.")
        email = input("Enter email: ")
        password = input("Enter password: ")
        if not LoginUser.login(email, password):
            print("Invalid login credentials. Exiting.")
            return
        print("Login successful!")
    else:
        print("Invalid choice. Exiting.")
        return

    from login import get_user_role  # Local import if needed
    user_role = get_user_role(email)
    if user_role is None:
        print("User role not found. Exiting.")
    elif user_role.lower() == "student":
        student_view(email)
    elif user_role.lower() == "professor":
        professor_view(email)
    elif user_role.lower() == "admin":
        admin_view()
    else:
        print("Role not recognized. Exiting.")

if __name__ == "__main__":
    main()
