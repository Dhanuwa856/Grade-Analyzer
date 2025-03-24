import pandas as pd
import numpy as np
import os

DATA_FILE = 'grades.csv'

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=['StudentID', 'Section', 'Sinhala', 'Math', 'Science', 'English'])


def grade_calculation(mark):
    return "A" if mark >= 75 else 'B' if mark >= 65 else 'C' if mark >= 50 else 'S' if mark >= 35 else 'W'


def format_output(lst):
    if not lst:
        return ""

    sorted_list = sorted(lst)

    result = []
    current_char = sorted_list[0]
    count = 1

    for char in sorted_list[1:]:
        if char == current_char:
            count += 1
        else:
            result.append(f"{count}{current_char}" if count > 1 else current_char)
            current_char = char
            count = 1

    result.append(f"{count}{current_char}" if count > 1 else current_char)

    return ",".join(result)
def get_student_report(df,student_id):
    student_data = df[df['StudentID'] == student_id]

    if student_data.empty:
        raise ValueError(f"Error: Student ID {student_id} not found!")

    student = student_data.iloc[0]
    print(f'Student ID: {student_id}')
    print(f"Class: {student['Section']}")
    print("Subject Marks:")
    grade = []
    marks = []
    for subject in ['Sinhala', 'Math', 'Science', 'English']:
        print(f"- {subject}: {student[subject]}")
        marks.append(student[subject])
        subject_grade = grade_calculation(int(student[subject]))
        grade.append(subject_grade)

    print(f"Grades: {format_output(grade)}")
    mean = np.mean(marks)
    print(f"Mean: {round(mean,1)}")




# try:
#     get_student_report("ST003")
# except ValueError as e:
#     print(e)

def save_data(df,student_id):
    df.to_csv(DATA_FILE,index=False)
    print(f'{student_id} Student successfully added!')


def add_student(df):
    print("\nEnter new student information:")

    while True:
        student_id = input("Student ID (e.g. ST005): ").strip().upper()
        if student_id in df['StudentID'].values:
            print(f"Error: {student_id} already exists!")
        else:
            break

    section = input("Section (e.g. 11A): ").strip().upper()

    def get_valid_mark(subject):
        while True:
            try:
                mark = int(input(f"{subject} mark: "))
                if 0 <= mark <= 100:
                    return mark
                else:
                     print("Score must be between 0-100!")
            except ValueError:
                print("Enter a Number!")

    sinhala = get_valid_mark("Sinhala")
    math = get_valid_mark("Mathematics")
    science = get_valid_mark("Science")
    english = get_valid_mark("English")

    new_student = pd.DataFrame([{
        'StudentID': student_id,
        'Section': section,
        'Sinhala': sinhala,
        'Math': math,
        'Science': science,
        'English': english
    }])

    df = pd.concat([df,new_student],ignore_index=True)
    save_data(df,student_id)


def view_students(df):
    print("\nAll Students:")
    print(df.to_string(index=False))

    search_id = input("\nEnter ID to search (leave blank): ").strip().upper()
    if search_id:
        result = df[df['StudentID'] == search_id]
        print("\nSearch results:" if not result.empty else "\nStudent not found!")
        print(result.to_string(index=False))

