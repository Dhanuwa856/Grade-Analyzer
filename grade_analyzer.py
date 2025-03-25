import pandas as pd
import numpy as np
import os

# Define the file name for storing student grades
DATA_FILE = 'grades.csv'

def load_data():
    """
    Load student data from the CSV file if it exists.
    Otherwise, return an empty DataFrame with specified columns.
    """
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        # Create a new DataFrame with the necessary columns if the file doesn't exist
        return pd.DataFrame(columns=['StudentID', 'Section', 'Sinhala', 'Math', 'Science', 'English'])

def grade_calculation(mark):
    """
    Calculate the grade based on the mark.
    - 'A' for marks 75 and above
    - 'B' for marks 65-74
    - 'C' for marks 50-64
    - 'S' for marks 35-49
    - 'W' for marks below 35
    """
    return "A" if mark >= 75 else 'B' if mark >= 65 else 'C' if mark >= 50 else 'S' if mark >= 35 else 'W'

def format_output(lst):
    """
    Format a list of grade letters into a compact string.
    For example, if lst = ['A', 'A', 'B', 'C', 'C'], the output will be "2A,B,2C".
    """
    if not lst:
        return ""

    # Sort the list so that same grades come together
    sorted_list = sorted(lst)

    result = []
    current_char = sorted_list[0]
    count = 1

    # Iterate over the sorted list and count consecutive occurrences
    for char in sorted_list[1:]:
        if char == current_char:
            count += 1
        else:
            # Append the count and grade if more than one, else just the grade
            result.append(f"{count}{current_char}" if count > 1 else current_char)
            current_char = char
            count = 1

    # Append the final group after the loop
    result.append(f"{count}{current_char}" if count > 1 else current_char)

    # Join the parts with commas
    return ",".join(result)

def get_student_report(df, student_id):
    """
    Print the report for a student given their ID.
    The report includes the student's section, marks for each subject,
    corresponding grades, and the mean of the marks.
    """
    # Filter the DataFrame for the given student_id
    student_data = df[df['StudentID'] == student_id]

    # If the student doesn't exist, raise an error
    if student_data.empty:
        raise ValueError(f"Error: Student ID {student_id} not found!")

    # Get the first (and only) matching record
    student = student_data.iloc[0]
    print(f'Student ID: {student_id}')
    print(f"Class: {student['Section']}")
    print("Subject Marks:")

    grade = []  # To store calculated grades for each subject
    marks = []  # To store marks for computing the mean

    # Loop through each subject and display marks and calculate grades
    for subject in ['Sinhala', 'Math', 'Science', 'English']:
        print(f"- {subject}: {student[subject]}")
        marks.append(student[subject])
        subject_grade = grade_calculation(int(student[subject]))
        grade.append(subject_grade)

    # Display the formatted grades and mean score
    print(f"Grades: {format_output(grade)}")
    mean = np.mean(marks)
    print(f"Mean: {round(mean, 1)}")

def save_data(df, student_id):
    """
    Save the DataFrame to the CSV file and print a confirmation message.
    """
    df.to_csv(DATA_FILE, index=False)
    print(f'{student_id} Student successfully added!')

def add_student(df):
    """
    Add a new student's information to the DataFrame.
    The function prompts the user for input, checks for duplicate student IDs,
    validates subject marks, and then saves the new student record.
    """
    print("\nEnter new student information:")

    # Ensure unique student ID
    while True:
        student_id = input("Student ID (e.g. ST005): ").strip().upper()
        if student_id in df['StudentID'].values:
            print(f"Error: {student_id} already exists!")
        else:
            break

    # Get student's section
    section = input("Section (e.g. 11A): ").strip().upper()

    def get_valid_mark(subject):
        """
        Prompt the user to enter a valid mark for a subject.
        The mark must be an integer between 0 and 100.
        """
        while True:
            try:
                mark = int(input(f"{subject} mark: "))
                if 0 <= mark <= 100:
                    return mark
                else:
                    print("Score must be between 0-100!")
            except ValueError:
                print("Enter a Number!")

    # Get validated marks for each subject
    sinhala = get_valid_mark("Sinhala")
    math = get_valid_mark("Mathematics")
    science = get_valid_mark("Science")
    english = get_valid_mark("English")

    # Create a new DataFrame for the new student record
    new_student = pd.DataFrame([{
        'StudentID': student_id,
        'Section': section,
        'Sinhala': sinhala,
        'Math': math,
        'Science': science,
        'English': english
    }])

    # Append the new student to the existing DataFrame
    df = pd.concat([df, new_student], ignore_index=True)
    # Save the updated DataFrame
    save_data(df, student_id)

def view_students(df):
    """
    Display all student records and allow the user to search for a specific student by ID.
    """
    print("\nAll Students:")
    print(df.to_string(index=False))

    # Prompt for a specific student ID to search for
    search_id = input("\nEnter ID to search (leave blank): ").strip().upper()
    if search_id:
        result = df[df['StudentID'] == search_id]
        # Show search results or a not-found message
        print("\nSearch results:" if not result.empty else "\nStudent not found!")
        print(result.to_string(index=False))


def update_student(df):
    # Prompt the user to enter the Student ID for the update
    student_id = input("Enter Student ID to update (e.g. ST001): ").strip().upper()

    # Check if the student exists in the DataFrame
    if student_id not in df['StudentID'].values:
        print("Student not found!")
        return df

    # Retrieve the student record as a Series (first occurrence)
    student = df[df['StudentID'] == student_id].iloc[0]

    # Display the current student information
    print("\nCurrent information:")
    print(student.to_string())

    # Ask for new information; if input is blank, keep the current value
    print("\nEnter new information (leave blank):")
    section = input(f"Class [{student['Section']}]: ").strip().upper() or student['Section']
    sinhala = input(f"Sinhala [{student['Sinhala']}]: ") or student['Sinhala']
    math = input(f"Mathematics [{student['Math']}]: ") or student['Math']
    science = input(f"Science [{student['Science']}]: ") or student['Science']
    english = input(f"English [{student['English']}]: ") or student['English']

    # Update the student's record in the DataFrame with the new values,
    # converting subject marks to integers
    df.loc[df['StudentID'] == student_id, ['Section', 'Sinhala', 'Math', 'Science', 'English']] = [
        section, int(sinhala), int(math), int(science), int(english)
    ]

    # Save the updated DataFrame to the CSV file and print a confirmation message
    save_data(df, student_id)
    return df


def delete_student(df):
    # Prompt the user for the Student ID to remove
    student_id = input("Need to remove Student ID (e.g. ST001): ").strip().upper()

    # Check if the student exists in the DataFrame
    if student_id not in df['StudentID'].values:
        print(f"Student not found with the application {student_id}!")
        return

    # Confirm removal from the user
    confirm = input(f"Do you want to permanently remove {student_id}? (Y/N): ").upper()
    if confirm != 'Y':
        print("Removal canceled")
        return

    # Remove the student from the DataFrame
    df = df[df['StudentID'] != student_id]

    # Update the CSV file to reflect the deletion
    df.to_csv(DATA_FILE, index=False)
    print(f"{student_id} student successfully removed!")

    return df
















