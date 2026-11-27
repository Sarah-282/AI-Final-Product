def calculate_grade(marks):
	"""Return the grade for a percentage."""
	if marks >= 90:
		return "A"
	elif marks >= 80:
		return "B"
	elif marks >= 70:
		return "C"
	elif marks >= 60:
		return "D"
	else:
		return "F"


def grading_system():
	print("Student Grading System")
	print("Enter marks for five subjects, each out of 100.")

	marks = []
	for subject_number in range(1, 6):
		while True:
			try:
				subject_marks = float(input(f"Subject {subject_number} marks: "))
				if 0 <= subject_marks <= 100:
					marks.append(subject_marks)
					break
				print("Marks must be between 0 and 100.")
			except ValueError:
				print("Please enter a valid number.")

	total_marks = sum(marks)
	percentage = total_marks / len(marks)
	grade = calculate_grade(percentage)

	print("\nResult")
	print(f"Total marks: {total_marks:g} / 500")
	print(f"Percentage: {percentage:.2f}%")
	print(f"Grade: {grade}")


if __name__ == "__main__":
	grading_system()
