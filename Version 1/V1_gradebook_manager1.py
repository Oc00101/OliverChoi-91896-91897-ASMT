# Gradebook Manager - Version 1

def add_student(gradebook):
    """
    Add a new student to the gradebook or update an existing student's scores.
    Prompts the user to input the student's name, age, and scores for multiple subjects.
    Validates inputs and stores the data in the gradebook dictionary.
    """
    name = input("Enter student's name: ").strip()  # Get and clean student name input
    if name in gradebook:
        print(f"Student {name} already exists. You can add or update their scores.")
    else:
        age = input("Enter student's age: ").strip()  # Get and clean age input
        if not age.isdigit():  # Validate age input
            print("Invalid age. Please enter a numeric value.") 
            return
        age = int(age)
        # put student basic details in gradebook
        gradebook[name] = {"age": age,
                           "subjects": {},
                           "total_score": 0,
                           "count_scores": 0
                           }

    # Loop to add/update subjects and scores for the student
    while True:
        subject = input("Enter subject name (or 'done' to finish): ").strip()
        if subject.lower() == 'done':
            break
        elif subject in gradebook[name]["subjects"]:
            print(f"Subject {subject} already exists for {name}. You can update the score.")
        elif subject == '': # Check if subject name is empty
            print("Invalid subject name. Please enter a valid subject.")
            continue
        score = input(f"Enter score for {subject}: ").strip()
        # Validate score input
        if not score.isdigit() or not (0 <= int(score) <= 100) or score == "":
            # Check if score is numeric and within valid range
            print("Invalid score. Please enter a numeric value between 0 and 100.")
            continue
        score = int(score)
        # Add/update subject score
        gradebook[name]["subjects"][subject] = score
        # Update total and count for average calculation
        gradebook[name]["total_score"] = sum(gradebook[name]["subjects"].values())
        gradebook[name]["count_scores"] = len(gradebook[name]["subjects"])

    print(f"Student {name} updated successfully!\n")
    display_and_save_summary(name, gradebook[name])  # Show and save summary


def calculate_average(subjects):
    """
    Calculate the average score for a student.
    Takes a dictionary of subjects and scores as input and returns the average score.
    """
    if not subjects:
        return 0
    # Calculate average if there are scores, else return 0
    return subjects["total_score"] / subjects["count_scores"] if subjects["count_scores"] > 0 else 0


def display_and_save_summary(name, data):
    """
    Display a summary report for a single student and save it to an external file.
    """
    print("\nSummary Report:")
    print(f"Name: {name}")
    print(f"Age: {data['age']}")
    print("Subjects and Scores:")
    for subject, score in data["subjects"].items():
        print(f"  {subject}: {score}")
    avg_score = calculate_average(data)
    print(f"Average Score: {avg_score:.2f}\n")

    # Save the summary to an external file for record-keeping
    with open("Version 1\gradebook_logs1.txt", "a") as file:
        file.write(f"Name: {name}\n")
        file.write(f"Age: {data['age']}\n")
        file.write("Subjects and Scores:\n")
        for subject, score in data["subjects"].items():
            file.write(f"  {subject}: {score}\n")
        file.write(f"Average Score: {avg_score:.2f}\n")
        file.write("-" * 40 + "\n")


def search_student():
    """
    Search for a student's summary in the external file and display it.
    """
    name = input("Enter the student's name to search: ").strip()  # Get student name to search
    try:
        with open("Version 1\gradebook_logs1.txt", "r") as file:
            summaries = file.read()  # Read all summaries
        if name in summaries:   
            print("\nStudent Summary Found:")
            start = summaries.find(f"Name: {name}")  # Find start of summary
            end = summaries.find("-" * 40, start)    # Find end of summary
            print(summaries[start:end])
        else:
            print(f"No summary found for student {name}.")
    except FileNotFoundError:
        print("No summaries file found. Please add students first.")


def main():
    """
    Main function to run the gradebook manager.
    Provides a menu-like interface for users to add students, search summaries, or exit.
    """
    gradebook = {}  # Initialize empty gradebook dictionary
    while True:
        print("\nGradebook Manager")
        print("1. Add/Update Student")
        print("2. Search Student Summary")  
        print("3. Exit")
        choice = input("Enter your choice (1-3): ").strip()
        if not choice.isdigit():
            print("Invalid choice. Please enter a numeric value.")
            continue
        choice = int(choice)
        if choice == 1:
            add_student(gradebook)  # Add or update student
        elif choice == 2:
            search_student()        # Search for student summary
        elif choice == 3:
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


# This ensures the main function runs only when the script is executed directly.
if __name__ == "__main__":
    main()