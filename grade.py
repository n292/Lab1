# grade.py
import csv
import os
import statistics
from collections import deque

def build_grade_hash_table():
    from student import Student 
    grade_table = {}
    students = Student.load_students()
    for student in students:
        for idx, course in enumerate(student.courses):
            if idx < len(student.marks):
                mark = student.marks[idx]
                if course not in grade_table:
                    grade_table[course] = deque()
                grade_table[course].append(mark)
    return grade_table
