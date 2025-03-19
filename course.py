
import csv
import os

class Course:
    def __init__(self, course_id, course_name, credits, description):
        self.course_id = course_id
        self.course_name = course_name
        self.credits = credits
        self.description = description

    def to_list(self):
        return [self.course_id, self.course_name, self.credits, self.description]

    @staticmethod
    def load_courses():
        courses = []
        if not os.path.exists("courses.csv"):
            return courses
        with open("courses.csv", "r") as file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader:
                if row:
                    courses.append(Course(*row))
        return courses

    @staticmethod
    def save_courses(courses):
        with open("courses.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Course ID", "Course Name", "Credits", "Description"])
            for course in courses:
                writer.writerow(course.to_list())

    @staticmethod
    def add_course(course):
        courses = Course.load_courses()
        for c in courses:
            if c.course_id == course.course_id:
                print("Course ID already exists!")
                return
        courses.append(course)
        Course.save_courses(courses)
        print("Course added successfully!")

    @staticmethod
    def delete_course(course_id):
        courses = Course.load_courses()
        updated_courses = [c for c in courses if c.course_id != course_id]
        if len(courses) == len(updated_courses):
            print("Course not found!")
            return
        Course.save_courses(updated_courses)
        print("Course deleted successfully!")

    @staticmethod
    def update_course(course_id, **kwargs):
        courses = Course.load_courses()
        found = False
        for course in courses:
            if course.course_id == course_id:
                for key, value in kwargs.items():
                    if hasattr(course, key):
                        setattr(course, key, value)
                found = True
                break
        if found:
            Course.save_courses(courses)
            print("Course record updated successfully!")
        else:
            print("Course not found!")

    @staticmethod
    def display_courses():
        courses = Course.load_courses()
        if not courses:
            print("No course records found.")
            return
        print("\n--- Course Records ---")
        for course in courses:
            print(f"ID: {course.course_id}, Name: {course.course_name}, Credits: {course.credits}, "
                  f"Description: {course.description}")
