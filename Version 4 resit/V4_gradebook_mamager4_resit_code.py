# Student Gradebook Manager – Version 4 
import json
import easygui as eg
import pandas as pd
import matplotlib.pyplot as plt

# Constants
AGE_MIN = 7
AGE_MAX = 18
SCORE_MIN = 0
SCORE_MAX = 100

# Load the gradebook data from a JSON file, or return an empty dict if file not found
def load_gradebook():
    try:
        with open("Version 4 resit/gradebook_logs.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Save the gradebook data to a JSON file
def save_gradebook(gradebook):
    with open("Version 4 resit/gradebook_logs.json", "w") as f:
        json.dump(gradebook, f, indent=2)

# Calculate the average score for a student
def calculate_average(student_data):
    if student_data["count_scores"] == 0:
        return 0
    return student_data["total_score"] / student_data["count_scores"]

# Display a summary of a student's info and plot their scores
def display_summary_and_plot(name, student_data):
    subjects = student_data["subjects"]
    summary = f"Name: {name}\nAge: {student_data['age']}\nSubjects and Scores:\n"
    for subject, score in subjects.items():
        summary += f"  {subject}: {score}\n"
    avg = calculate_average(student_data)
    summary += f"Average Score: {avg:.2f}"
    eg.msgbox(summary, title="Student Summary")

    # Plot the student's scores if there are any subjects
    if subjects:
        # Convert subjects dict to DataFrame for easier plotting
        df = pd.DataFrame(subjects.items(), columns=["Subject", "Score"])
        plt.figure(figsize=(8, 4))
        plt.bar(df["Subject"], df["Score"], color="skyblue")
        plt.title(f"{name}'s Scores")
        plt.xlabel("Subject")
        plt.ylabel("Score")
        plt.ylim(0, 100)
        plt.tight_layout()
        plt.show()

# Add a new student or update an existing student's info and scores
def add_student(gradebook):
    name = eg.enterbox("Enter student's name:")
    if not name:
        eg.msgbox("Name cannot be blank.")
        return
    name = name.strip().lower()  # Make name case-insensitive

    if name in gradebook:
        eg.msgbox(f"Student {name.title()} already exists. You can add or update their scores.")
    else:
        while True:
            age_input = eg.enterbox(f"Enter student's age ({AGE_MIN}-{AGE_MAX}):")
            # Validate age input: must be a digit and within a reasonable range
            if not age_input or not age_input.isdigit():
                eg.msgbox("Invalid input. Please enter a number.")
                continue
            age = int(age_input)
            if age < AGE_MIN or age > AGE_MAX:
                eg.msgbox(f"Age must be between {AGE_MIN} and {AGE_MAX}.")
                continue
            break
        # Initialize student data structure
        gradebook[name] = {"age": age, "subjects": {}, "total_score": 0, "count_scores": 0}

    # Loop to add subjects and scores
    while True:
        subject = eg.enterbox("Enter subject name (or leave blank to finish):")
        if not subject:
            break
        subject = subject.strip().lower()  # Make subject case-insensitive
        while True:
            score_input = eg.enterbox(f"Enter score for {subject.title()} ({SCORE_MIN}-{SCORE_MAX}):")
            # Validate score input
            if not score_input or not score_input.isdigit():
                eg.msgbox("Invalid input. Please enter a number.")
                continue
            score = int(score_input)
            if score < SCORE_MIN or score > SCORE_MAX:
                eg.msgbox(f"Score must be between {SCORE_MIN} and {SCORE_MAX}.")
                continue
            break
        gradebook[name]["subjects"][subject] = score
        # Update total and count for average calculation
        gradebook[name]["total_score"] = sum(gradebook[name]["subjects"].values())
        gradebook[name]["count_scores"] = len(gradebook[name]["subjects"])

    eg.msgbox(f"Student {name.title()} updated successfully!")
    save_gradebook(gradebook)

# Edit an existing student's age or subjects/scores, or delete subjects
def edit_student(gradebook):
    name = eg.enterbox("Enter the student’s name to edit:")
    if not name:
        return
    name = name.strip().lower()
    if name not in gradebook:
        eg.msgbox(f"{name.title()} not found.")
        return

    student = gradebook[name]
    # Loop to edit age
    while True:
        age_input = eg.enterbox(f"Current age is {student['age']}. Enter new age or leave blank:")
        if not age_input:
            eg.msgbox("Age not changed.")
            break
        if age_input.isdigit():
            new_age = int(age_input)
            if AGE_MIN <= new_age <= AGE_MAX:
                student['age'] = new_age
                break
            else:
                eg.msgbox(f"Age must be between {AGE_MIN} and {AGE_MAX}.")
        else:
            eg.msgbox("Invalid age input.")
            

    # Loop to edit or delete subjects
    while True:
        subject = eg.enterbox("Enter subject to edit or delete (or leave blank to finish):")
        if not subject:
            break
        subject = subject.strip().lower()
        if subject not in student['subjects']:
            eg.msgbox("Subject not found.")
            continue
        while True:
            score_input = eg.enterbox(f"Current score is {student['subjects'][subject]}. Enter new score or leave blank to delete:")
            # If blank, delete the subject
            if not score_input:
                del student['subjects'][subject]
                break
            # If valid score, update it
            elif score_input.isdigit():
                score = int(score_input)
                if SCORE_MIN <= score <= SCORE_MAX:
                    student['subjects'][subject] = score
                    break
                else:
                    eg.msgbox(f"Invalid score, score must be between {SCORE_MIN} and {SCORE_MAX}.")
            else:
                eg.msgbox(f"Invalid score, score must be an integer and between {SCORE_MIN} and {SCORE_MAX}.")

    # Update total and count after editing
    student['total_score'] = sum(student['subjects'].values())
    student['count_scores'] = len(student['subjects'])
    save_gradebook(gradebook)
    eg.msgbox(f"Student {name.title()} updated.")

# Search for a student by name and display their summary and plot
def search_student(gradebook):
    student_name = eg.enterbox("Enter the student's name to search:")
    if not student_name:
        return
    student_name = student_name.strip().lower()
    for name in gradebook:
        if name == student_name:
            display_summary_and_plot(name.title(), gradebook[name])
            return
    eg.msgbox(f"No summary found for student '{student_name.title()}'.")

# View a list of all students in the gradebook
def view_all_students(gradebook):
    if not gradebook:
        eg.msgbox("No students in the gradebook.")
        return
    # Show all student names (keys of the gradebook)
    student_list = "\n".join(name.title() for name in gradebook.keys())
    eg.textbox("All Students:", text=student_list)

# Main program loop: show menu and call functions based on user choice
def main():
    gradebook = load_gradebook()
    while True:
        choice = eg.buttonbox("Choose an option:", choices=[
            "Add/Update Student",
            "Edit/Delete Student",
            "Search Student",
            "View All Students",
            "Exit"
        ], title="Student Gradebook Manager")
        if choice == "Add/Update Student":
            add_student(gradebook)
        elif choice == "Edit/Delete Student":
            edit_student(gradebook)
        elif choice == "Search Student":
            search_student(gradebook)
        elif choice == "View All Students":
            view_all_students(gradebook)
        elif choice == "Exit":
            save_gradebook(gradebook)
            eg.msgbox("Exiting the program. Goodbye!")
            break

# Run the program if this file is executed directly
if __name__ == "__main__":
    main()
