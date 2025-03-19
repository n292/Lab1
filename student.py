# student.py
import csv
import os
import time
import statistics
from collections import deque
from grade import build_grade_hash_table

class Student:
    def __init__(self, student_id, email, first_name, last_name, courses, grades, marks):
        self.student_id = student_id
        self.email_address = email
        self.first_name = first_name
        self.last_name = last_name

        if isinstance(courses, str):
            delimiter = ',' if ',' in courses else ';'
            self.courses = [c.strip() for c in courses.split(delimiter) if c.strip()]
        else:
            self.courses = courses

        if isinstance(grades, str):
            delimiter = ',' if ',' in grades else ';'
            self.grades = [g.strip() for g in grades.split(delimiter) if g.strip()]
        else:
            self.grades = grades

        if isinstance(marks, str):
            delimiter = ',' if ',' in marks else ';'
            try:
                self.marks = [int(m.strip()) for m in marks.split(delimiter) if m.strip()]
            except ValueError as e:
                print("Error converting marks to integers:", e)
                self.marks = []
        else:
            self.marks = marks

    def to_list(self):
        courses_str = ';'.join(self.courses)
        grades_str = ';'.join(self.grades)
        marks_str = ';'.join(str(m) for m in self.marks)
        return [self.student_id, self.email_address, self.first_name, self.last_name, courses_str, grades_str, marks_str]

    @staticmethod
    def load_students():
        students = []
        if not os.path.exists("students.csv"):
            return students
        with open("students.csv", "r") as file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader:
                if row:
                    students.append(Student(*row))
        return students

    @staticmethod
    def save_students(students):
        with open("students.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Student ID", "Email", "First Name", "Last Name", "Courses", "Grades", "Marks"])
            for student in students:
                writer.writerow(student.to_list())

    @staticmethod
    def add_student(student):
        students = Student.load_students()
        for s in students:
            if s.student_id == student.student_id:
                print("Student ID already exists!")
                return
        students.append(student)
        Student.save_students(students)
        print("Student added successfully!")

    @staticmethod
    def delete_student(student_id):
        students = Student.load_students()
        updated_students = [s for s in students if s.student_id != student_id]
        if len(students) == len(updated_students):
            print("Student not found!")
            return
        Student.save_students(updated_students)
        print("Student deleted successfully!")

    @staticmethod
    def update_student(student_id, **kwargs):
        students = Student.load_students()
        found = False
        for student in students:
            if student.student_id == student_id:
                for key, value in kwargs.items():
                    if hasattr(student, key):
                        if key == "marks":
                            student.marks = [int(m.strip()) for m in value.split(',') if m.strip()]
                        elif key in ("courses", "grades"):
                            setattr(student, key, [x.strip() for x in value.split(',') if x.strip()])
                        else:
                            setattr(student, key, value)
                found = True
                break
        if found:
            Student.save_students(students)
            print("Student record updated successfully!")
        else:
            print("Student not found!")

    @staticmethod
    def display_students():
        students = Student.load_students()
        if not students:
            print("No student records found.")
            return
        print("\n--- Student Records ---")
        for student in students:
            print(f"ID: {student.student_id}")
            print(f"Name: {student.first_name} {student.last_name}")
            print(f"Email: {student.email_address}")
            print("Courses and Grades:")
            for i, course in enumerate(student.courses):
                grade = student.grades[i] if i < len(student.grades) else "N/A"
                mark = student.marks[i] if i < len(student.marks) else "N/A"
                print(f"  - {course}: Grade {grade}, Marks {mark}")
            print("-" * 40)

    @staticmethod
    def search_student_by_name(name):
        start_time = time.perf_counter()
        students = Student.load_students()
        results = [s for s in students if s.first_name.lower() == name.lower()]
        end_time = time.perf_counter()
        search_time = end_time - start_time

        print(f"Search completed in {search_time:.6f} seconds")
        if results:
            for student in results:
                print(f"ID: {student.student_id}, Name: {student.first_name} {student.last_name}")
        else:
            print(f"No student found: {name}")

    @staticmethod
    def sort_students_by_name():
        students = Student.load_students()
        students.sort(key=lambda s: s.first_name.lower())
        print("\n--- Students Sorted by Name ---")
        for student in students:
            print(f"ID: {student.student_id}, Name: {student.first_name} {student.last_name}, Courses: {', '.join(student.courses)}")

    @staticmethod
    def compute_average_marks_for_course(course_id):
        grade_table = build_grade_hash_table()
        if course_id in grade_table and grade_table[course_id]:
            marks_list = list(grade_table[course_id])
            avg = sum(marks_list) / len(marks_list)
            print(f"Average Marks for course {course_id}: {avg:.2f}")
            return avg
        else:
            print("No scores available for this course.")
            return 0

    @staticmethod
    def compute_median_marks_for_course(course_id):
        grade_table = build_grade_hash_table()
        if course_id in grade_table and grade_table[course_id]:
            marks_list = list(grade_table[course_id])
            med = statistics.median(marks_list)
            print(f"Median scores for course {course_id}: {med}")
            return med
        else:
            print("No scores available for this course.")
            return 0

    @staticmethod
    def get_student_by_email(email):
        students = Student.load_students()
        for s in students:
            if s.email_address.lower() == email.lower():
                return s
        return None
