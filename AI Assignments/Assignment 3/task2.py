def sort_student_marks(students):
	"""Return students sorted from highest mark to lowest mark.

	Each student must be a dictionary with a name and marks from 0 to 100.
	The original list is not changed.
	"""
	for student in students:
		if not 0 <= student["marks"] <= 100:
			raise ValueError("Marks must be between 0 and 100.")

	return sorted(students, key=lambda student: student["marks"], reverse=True)


# Refined prompt requirements:
# - Sort student marks in descending order, from highest to lowest.
# - Accept student names and marks as records.
# - Allow marks only in the range 0 to 100.
# - Keep the original input list unchanged.
students = [
	{"name": "Aisha", "marks": 82},
	{"name": "Ben", "marks": 95},
	{"name": "Carlos", "marks": 74},
]

sorted_students = sort_student_marks(students)

for student in sorted_students:
	print(f"{student['name']}: {student['marks']}")
