# Student Gradebook Manager – Version 3 
import json
import easygui as eg

# Loads the gradebook data from a JSON file.
# Returns a dictionary of students and their data.
def load_gradebook():
    try:
        with open("Version 3/gradebook_logs.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        # If the file doesn't exist, return an empty gradebook.
        return {}

# Saves the current gradebook dictionary to a JSON file.
def save_gradebook(gradebook):
    with open("Version 3/gradebook_logs.json", "w") as f:
        json.dump(gradebook, f, indent=2)

# Adds a new student or updates an existing student's scores.
# Prompts for name, age, subjects, and scores using GUI dialogs.
def add_student(gradebook):
    name = eg.enterbox("Enter student's name:")
    if not name:
        eg.msgbox("Name cannot be blank.")
        return

    if name in gradebook:
        # If student exists, allow updating their scores.
        eg.msgbox(f"Student {name} already exists. You can add or update their scores.")
    else:
        # For new students, prompt for age and validate input.
        age_input = eg.enterbox("Enter student's age:")
        if not age_input or not age_input.isdigit() or not (1 <= int(age_input) <= 120):
            eg.msgbox("Invalid age. Please enter a number between 1 and 120.")
            return
        age = int(age_input)
        # Initialize student record.
        gradebook[name] = {"age": age, 
                           "subjects": {}, 
                           "total_score": 0, 
                           "count_scores": 0
                           }

    # Loop to add or update subjects and scores.
    while True:
        subject = eg.enterbox("Enter subject name (or leave blank to finish):")
        if subject == "":
            break
        score_input = eg.enterbox(f"Enter score for {subject} (0 to 100):")
        if not score_input or not score_input.isdigit() or not (0 <= int(score_input) <= 100):
            eg.msgbox("Invalid score. Please enter a number between 0 and 100.")
            continue
        score = int(score_input)
        gradebook[name]["subjects"][subject] = score
        # Update total and count for average calculation.
        gradebook[name]["total_score"] = sum(gradebook[name]["subjects"].values())
        gradebook[name]["count_scores"] = len(gradebook[name]["subjects"])

    eg.msgbox(f"Student {name} updated successfully!")
    save_gradebook(gradebook)

# Calculates the average score for a student.
def calculate_average(student_data):
    if student_data["count_scores"] == 0:
        return 0
    return student_data["total_score"] / student_data["count_scores"]

# Displays a summary of a student's information and scores.
def display_summary(name, student_data):
    summary = f"Name: {name}\nAge: {student_data['age']}\nSubjects and Scores:\n"
    for subject, score in student_data["subjects"].items():
        summary += f"  {subject}: {score}\n"
    avg = calculate_average(student_data)
    summary += f"Average Score: {avg:.2f}"
    eg.msgbox(summary, title="Student Summary")

# Allows editing a student's age, subjects, or deleting subjects.
def edit_student(gradebook):
    name = eg.enterbox("Enter the student’s name to edit:")
    if not name or name not in gradebook:
        eg.msgbox(f"{name} not found.")
        return

    student = gradebook[name]
    # Optionally update age.
    age_input = eg.enterbox(f"Current age is {student['age']}. Enter new age or leave blank:")
    if age_input is not None and age_input.isdigit():
        student['age'] = int(age_input)
    elif age_input == "":
        # If input is blank, keep the current age.
        pass
    
    # Loop to edit or delete subjects.
    while True:
        subject = eg.enterbox("Enter subject to edit or delete (or leave blank to finish):")
        if not subject:
            break
        if subject not in student['subjects']:
            eg.msgbox("Subject not found.")
            continue
        score_input = eg.enterbox(f"Current score is {student['subjects'][subject]}. Enter new score or leave blank to delete:")
        if not score_input:
            # Delete subject if input is blank.
            del student['subjects'][subject]
        elif score_input.isdigit() and 0 <= int(score_input) <= 100:
            # Update score if valid.
            student['subjects'][subject] = int(score_input)

    # Update totals after editing.
    student['total_score'] = sum(student['subjects'].values())
    student['count_scores'] = len(student['subjects'])
    save_gradebook(gradebook)
    eg.msgbox(f"Student {name} updated.")

# Searches for a student by name (case-insensitive) and displays their summary.
def search_student(gradebook):
    student_name = eg.enterbox("Enter the student's name to search:")
    if not student_name:
        return
    for name in gradebook:
        if name.lower() == student_name.lower():
            display_summary(name, gradebook[name])  # Use the actual key
            return
    eg.msgbox(f"No summary found for student '{student_name}'.")

# Shows a list of all students in the gradebook.
def view_all_students(gradebook):
    if not gradebook:
        eg.msgbox("No students in the gradebook.")
        return
    student_list = "\n".join(gradebook.keys())
    eg.textbox("All Students:", text=student_list)

# Main loop for the gradebook manager.
# Presents a menu and calls the appropriate function based on user choice.
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

# runs the main function if this script is executed directly.
if __name__ == "__main__":
    main()