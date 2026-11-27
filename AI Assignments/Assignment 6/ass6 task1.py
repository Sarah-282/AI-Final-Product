class Student:
	def __init__(self, name, roll_no, marks):
		self.name = name
		self.roll_no = roll_no
		self.marks = marks

	def is_pass(self):
		return self.marks >= 40
