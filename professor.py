# professor.py
import csv
import os

class Professor:
    def __init__(self, professor_id, name, email, rank, courses):
        self.professor_id = professor_id
        self.name = name
        self.email = email
        self.rank = rank
        if isinstance(courses, str):
            delimiter = ',' if ',' in courses else ';'
            self.courses = [c.strip() for c in courses.split(delimiter) if c.strip()]
        else:
            self.courses = courses

    def to_list(self):
        courses_str = ';'.join(self.courses)
        return [self.professor_id, self.name, self.email, self.rank, courses_str]

    @staticmethod
    def load_professors():
        professors = []
        if not os.path.exists("professors.csv"):
            return professors
        with open("professors.csv", "r") as file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader:
                if row:
                    professors.append(Professor(*row))
        return professors

    @staticmethod
    def save_professors(professors):
        with open("professors.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Professor ID", "Name", "Email", "Rank", "Courses"])
            for professor in professors:
                writer.writerow(professor.to_list())

    @staticmethod
    def add_professor(professor):
        professors = Professor.load_professors()
        for p in professors:
            if p.professor_id == professor.professor_id:
                print("Professor ID already exists!")
                return
        professors.append(professor)
        Professor.save_professors(professors)
        print("Professor added successfully!")

    @staticmethod
    def delete_professor(professor_id):
        professors = Professor.load_professors()
        updated_professors = [p for p in professors if p.professor_id != professor_id]
        if len(professors) == len(updated_professors):
            print("Professor not found!")
            return
        Professor.save_professors(updated_professors)
        print("Professor deleted successfully!")

    @staticmethod
    def update_professor(professor_id, **kwargs):
        professors = Professor.load_professors()
        found = False
        for professor in professors:
            if professor.professor_id == professor_id:
                for key, value in kwargs.items():
                    if hasattr(professor, key):
                        if key == "courses":
                            professor.courses = [x.strip() for x in value.split(',') if x.strip()]
                        else:
                            setattr(professor, key, value)
                found = True
                break
        if found:
            Professor.save_professors(professors)
            print("Professor record updated successfully!")
        else:
            print("Professor not found!")

    @staticmethod
    def display_professors():
        professors = Professor.load_professors()
        if not professors:
            print("No professor records found.")
            return
        print("\n--- Professor Records ---")
        for professor in professors:
            print(f"ID: {professor.professor_id}, Name: {professor.name}, Email: {professor.email}, "
                  f"Rank: {professor.rank}, Courses: {', '.join(professor.courses)}")

    @staticmethod
    def get_professor_by_email(email):
        professors = Professor.load_professors()
        for p in professors:
            if p.email.lower() == email.lower():
                return p
        return None
