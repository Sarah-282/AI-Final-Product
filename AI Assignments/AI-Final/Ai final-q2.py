import math


class Student:
	def __init__(self, name, roll_no, marks):
		if not isinstance(name, str) or not name.strip():
			raise ValueError("name must be a non-empty string")
		if not isinstance(roll_no, int) or isinstance(roll_no, bool):
			raise TypeError("roll_no must be an integer")
		if not isinstance(marks, (int, float)) or isinstance(marks, bool):
			raise TypeError("marks must be a number")
		if not 0 <= marks <= 100:
			raise ValueError("marks must be between 0 and 100")

		self.name = name
		self.roll_no = roll_no
		self.marks = marks

	def is_pass(self):
		return self.marks >= 40


# Prompt refinement:
# Vague: "Sort the students by their marks."
# Refined: "Return a new list of Student objects sorted by marks from highest
# to lowest by default, optionally lowest to highest, with marks constrained
# to the validated 0-100 range and original input order preserved for ties."
def sort_students_by_marks(students, descending=True):
	"""Return students sorted by marks without modifying the input list.

	Example: ``sort_students_by_marks(students)`` places the highest mark first.
	Pass ``descending=False`` to sort from lowest to highest.
	"""
	if not isinstance(students, (list, tuple)):
		raise TypeError("students must be a list or tuple of Student objects")
	if not isinstance(descending, bool):
		raise TypeError("descending must be a boolean")
	if not all(isinstance(student, Student) for student in students):
		raise TypeError("students must contain only Student objects")

	return sorted(students, key=lambda student: student.marks, reverse=descending)


class Circle:
	def __init__(self, radius):
		self.radius = radius

	def area(self):
		return math.pi * self.radius ** 2

	def circumference(self):
		return 2 * math.pi * self.radius


def print_triangle_for(rows):
	for row in range(1, rows + 1):
		print("*" * row)


def print_triangle_while(rows):
	row = 1
	while row <= rows:
		print("*" * row)
		row += 1


def analyze_number(number):
	if number > 0:
		return "positive"
	elif number < 0:
		return "negative"
	else:
		return "zero"


def is_prime(number):
	"""Return whether an integer is prime.

	Few-shot examples:

		>>> is_prime(-3)
		False
		>>> is_prime(0)
		False
		>>> is_prime(1)
		False
		>>> is_prime(2)
		True
		>>> is_prime(9)
		False
		>>> is_prime(97)
		True

	The examples clarify that prime numbers are integers greater than one with
	no divisors other than one and themselves.
	"""
	if not isinstance(number, int) or isinstance(number, bool):
		raise TypeError("number must be an integer")
	if number < 2:
		return False

	for divisor in range(2, int(number ** 0.5) + 1):
		if number % divisor == 0:
			return False
	return True


def check_discount(age, is_member):
	if age >= 60:
		if is_member:
			return "Senior discount and additional member discount"
		else:
			return "Senior discount"
	else:
		if is_member:
			return "Additional member discount"
		else:
			return "No discount"


if __name__ == "__main__":
	students = [
		Student("Ali", 1, 75),
		Student("Sara", 2, 35),
		Student("John", 3, 40),
	]

	for student in students:
		status = "Passed" if student.is_pass() else "Failed"
		print(f"{student.name}: {status}")

	print("\nPattern using a for loop:")
	print_triangle_for(5)

	print("\nPattern using a while loop:")
	print_triangle_while(5)

	print("\nNumber analysis:")
	for number in (10, -3, 0):
		print(f"{number} is {analyze_number(number)}")

	print("\nDiscount eligibility:")
	for age, is_member in ((65, True), (65, False), (30, True), (30, False)):
		print(f"Age {age}, member: {is_member} -> {check_discount(age, is_member)}")

	circle = Circle(5)
	print("\nCircle calculations:")
	print(f"Area: {circle.area():.2f}")
	print(f"Circumference: {circle.circumference():.2f}")

		
