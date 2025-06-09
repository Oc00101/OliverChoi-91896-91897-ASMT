# Student Gradebook Manager – Version 2 

import easygui as eg  # Import the EasyGUI library for GUI dialogs

def add_student(gradebook):
    """
    Add a new student to the gradebook or update an existing student's scores.
    Prompts the user to input the student's name, age, and scores for multiple subjects.
    Validates inputs and stores the data in the gradebook dictionary.
    """    
    name = eg.enterbox("Enter student's name:") # Prompt user to enter student's name
    if name == "":
        eg.msgbox("Name cannot be blank.")
        return

    # Check if student already exists
    if name in gradebook:
        eg.msgbox(f"Student {name} already exists. You can add or update their scores.")
    else:
        # Prompt for age if new student
        age_input = eg.enterbox("Enter student's age:")
        if not age_input or not age_input.isdigit():
            eg.msgbox("Invalid age. Please enter a number.")
            return
        age = int(age_input)
        # Initialize student data
        gradebook[name] = {"age": age,
                           "subjects": {},
                           "total_score": 0,
                           "count_scores": 0
                           }

    # Loop to add subjects and scores
    while True:
        subject = eg.enterbox("Enter subject name (or leave blank to finish):")
        if not subject:
            break
        score_input = eg.enterbox(f"Enter score for {subject} (0 to 100):")
        if not score_input or not score_input.isdigit() or not (0 <= int(score_input) <= 100):
            eg.msgbox("Invalid score. Please enter a number between 0 and 100.")
            continue
        score = int(score_input)
        # Update subject and scores
        gradebook[name]["subjects"][subject] = score
        gradebook[name]["total_score"] = sum(gradebook[name]["subjects"].values())
        gradebook[name]["count_scores"] = len(gradebook[name]["subjects"])

    eg.msgbox(f"Student {name} updated successfully!")
    display_and_save_summary(name, gradebook[name])

def calculate_average(student_data):
    # Calculate the average score for a student
    if student_data["count_scores"] == 0:
        return 0
    return student_data["total_score"] / student_data["count_scores"]

def display_and_save_summary(name, student_data):
    # Create a summary string for the student
    summary = f"Name: {name}\nAge: {student_data['age']}\nSubjects and Scores:\n"
    for subject, score in student_data["subjects"].items():
        summary += f"  {subject}: {score}\n"
    avg = calculate_average(student_data)
    summary += f"Average Score: {avg:.2f}"

    # Display the summary in a message box
    eg.msgbox(summary, title="Student Summary")

    # Save the summary to an external file
    with open("Version 2\gradebook_logs.txt", "a") as file:
        file.write(f"{summary}\n{'-' * 40}\n")

def search_student():
    # Prompt user to enter the student's name to search
    name = eg.enterbox("Enter the student's name to search:")
    if not name:
        return
    try:
        # Read summaries from the log file
        with open("Version 2\gradebook_logs.txt", "r") as file:
            summaries = file.read()
        # Search for the student's summary
        if name in summaries:
            start = summaries.find(f"Name: {name}")
            end = summaries.find("-" * 40, start)
            result = summaries[start:end] if end != -1 else summaries[start:]
            eg.msgbox(result.strip(), title="Search Result")
        else:
            eg.msgbox(f"No summary found for student '{name}'.")
    except FileNotFoundError:
        eg.msgbox("No summaries file found. Please add students first.")

def main():
    # Main program loop
    gradebook = {}
    while True:
        # Show main menu options
        choice = eg.buttonbox("Choose an option:", choices=["Add/Update Student", "Search Student Summary", "Exit"], title="Student Gradebook Manager")
        if choice == "Add/Update Student":
            add_student(gradebook)
        elif choice == "Search Student Summary":
            search_student()
        elif choice == "Exit":
            eg.msgbox("Exiting the program. Goodbye!")
            break

if __name__ == "__main__":
    main()
