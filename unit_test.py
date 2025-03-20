import unittest
import time
from student import Student
from course import Course
from professor import Professor
from login import LoginUser, get_user_role
from grade import build_grade_hash_table

class TestCheckMyGrade(unittest.TestCase):


    def test_student_records_crud_and_1000_records(self):
        students = Student.load_students()
        initial_count = len(students)
        print(f"Initial student count: {initial_count}")
        
        if initial_count < 1000:
            for i in range(initial_count, 1000):
                student_id = f"student_{i}"
                if not any(s.student_id == student_id for s in Student.load_students()):
                    s = Student(student_id, f"student{i}@college.com", f"Student{i}", f"Lastname{i}", "DATA200", "A", "93")
                    Student.add_student(s)
                    print(f"Added student: {student_id}")

        students_after = Student.load_students()
        self.assertGreaterEqual(len(students_after), 1000, "Student records are less than 1000 after additions.")

        Student.update_student("student_0", first_name="UpdatedStudent0")
        updated_student = None
        for s in Student.load_students():
            if s.student_id == "student_0":
                updated_student = s
                break
        self.assertIsNotNone(updated_student, "Student record student_0 not found after update.")
        self.assertEqual(updated_student.first_name, "UpdatedStudent0")
        print(f"Updated Student ID: {updated_student.student_id}, New Name: {updated_student.first_name}")

        Student.delete_student("student_0")
        students_after_deletion = Student.load_students()
        found = any(s.student_id == "student_0" for s in students_after_deletion)
        self.assertFalse(found, "Student record student_0 was not deleted.")
        print(f"Deleted Student ID: student_0")

        start_time = time.perf_counter()
        search_name = "Student10"
        print(f"Searching for students with name: {search_name}")
        Student.search_student_by_name(search_name)
        end_time = time.perf_counter()
        search_time = end_time - start_time
        print(f"Total time taken for student search: {search_time:.6f} seconds")


    def test_sort_student_records_by_email(self):
        students = Student.load_students()
        start_time = time.perf_counter()
        sorted_students = sorted(students, key=lambda s: s.email_address.lower())
        end_time = time.perf_counter()
        sort_time = end_time - start_time
        print(f"Total time taken to sort student records by email: {sort_time:.6f} seconds")

        sorted_emails = [s.email_address.lower() for s in sorted_students]
        self.assertEqual(sorted_emails, sorted(sorted_emails), "Students are not sorted correctly by email.")

        # Print sorted students
        print("\n--- Sorted Students by Email ---")
        for student in sorted_students[:10]:  # Print only the first 10 for brevity
            print(f"ID: {student.student_id}, Email: {student.email_address}")
    
    
    
    def test_course_crud(self):
        course = Course("course_test", "Test Course", "3", "Course for testing CRUD")
        Course.add_course(course)
        courses = Course.load_courses()
        self.assertTrue(any(c.course_id == "course_test" for c in courses), "Course was not added correctly.")
        print(f"Added Course: {course.course_id}")

        Course.update_course("course_test", description="intro to python")
        updated_course = next((c for c in Course.load_courses() if c.course_id == "course_test"), None)
        self.assertEqual(updated_course.description, "Updated description")
        print(f"Updated Course ID: {updated_course.course_id}, New Description: {updated_course.description}")

        Course.delete_course("course_test")
        courses_after_delete = Course.load_courses()
        deleted = not any(c.course_id == "course_test" for c in courses_after_delete)
        self.assertTrue(deleted, "Course was not deleted correctly.")
        print(f"Deleted Course ID: course_test, Name: Test Course")

    def test_professor_crud(self):
        professor = Professor("prof_test", "Prof Test", "prof@test.com", "Assistant", "CS101")
        Professor.add_professor(professor)
        professors = Professor.load_professors()
        self.assertTrue(any(p.professor_id == "prof_test" for p in professors), "Professor was not added correctly.")
        print(f"Added Professor: {professor.professor_id}, Name: {professor.name}")

        Professor.update_professor("prof_test", name="Prof Updated")
        updated_professor = next((p for p in Professor.load_professors() if p.professor_id == "prof_test"), None)
        self.assertEqual(updated_professor.name, "Prof Updated")
        print(f"Updated Professor ID: {updated_professor.professor_id}, New Name: {updated_professor.name}")

        Professor.delete_professor("prof_test")
        professors_after_delete = Professor.load_professors()
        deleted = not any(p.professor_id == "prof_test" for p in professors_after_delete)
        self.assertTrue(deleted, "Professor was not deleted correctly.")
        print(f"Deleted Professor ID: prof_test, Name: Prof Updated")

        

    def test_login_functionality(self):
        
        user_email = "nikhil@sjsu.edu"
        user_password = "nikhil"
        user_role = "admin"
        new_user = LoginUser(user_email, user_password, user_role)
        LoginUser.register_user(new_user)

        
        login_success = LoginUser.login(user_email, user_password)
        self.assertTrue(login_success, "User login failed after registration.")

       
        encrypted_password = None
        with open("login.csv", "r") as file:
            lines = file.readlines()
            for line in lines:
                if user_email in line:
                    encrypted_password = line.split(",")[1].strip()
                    break

        self.assertIsNotNone(encrypted_password, "Encrypted password not found in login.csv")
        self.assertNotEqual(user_password, encrypted_password, "Password was not encrypted in login.csv")

        decrypted_password = LoginUser.decrypt_password(encrypted_password)
        self.assertEqual(user_password, decrypted_password, "Password decryption failed.")

       
        retrieved_role = get_user_role(user_email)
        self.assertEqual(retrieved_role, user_role, "User role retrieval failed.")

if __name__ == "__main__":
    unittest.main()
