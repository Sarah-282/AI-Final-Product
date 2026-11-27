def calculator(first_number, operator, second_number):
	"""Perform a basic arithmetic calculation."""
	# Select the operation requested by the user.
	if operator == "+":
		return first_number + second_number
	elif operator == "-":
		return first_number - second_number
	elif operator == "*":
		return first_number * second_number
	elif operator == "/":
		if second_number == 0:
			return "Error: cannot divide by zero."
		return first_number / second_number
	else:
		return "Error: unsupported operator."


# Usage examples added after the function was designed:
print(calculator(10, "+", 5))
print(calculator(10, "-", 5))
print(calculator(10, "*", 5))
print(calculator(10, "/", 5))
print(calculator(10, "/", 0))
