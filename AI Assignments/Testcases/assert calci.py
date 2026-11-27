def calculate(first, operator, second):
	"""Return the result of a basic arithmetic operation."""
	if operator == "+":
		return first + second
	if operator == "-":
		return first - second
	if operator == "*":
		return first * second
	if operator == "/":
		if second == 0:
			raise ZeroDivisionError("Cannot divide by zero")
		return first / second
	raise ValueError("Unsupported operation. Use +, -, *, or /.")


def factorial(number):
	"""Return the factorial of a non-negative integer."""
	if not isinstance(number, int) or isinstance(number, bool):
		raise TypeError("number must be an integer")
	if number < 0:
		raise ValueError("number must be non-negative")

	result = 1
	for factor in range(2, number + 1):
		result *= factor
	return result


def run_assert_tests():
	assert calculate(2, "+", 3) == 5
	assert calculate(5, "-", 3) == 2
	assert calculate(4, "*", 3) == 12
	assert calculate(8, "/", 2) == 4
	assert calculate(-2, "+", 5) == 3

	try:
		calculate(1, "/", 0)
	except ZeroDivisionError:
		pass
	else:
		raise AssertionError("Division by zero should raise ZeroDivisionError")

	try:
		calculate(2, "%", 3)
	except ValueError:
		pass
	else:
		raise AssertionError("An unsupported operation should raise ValueError")

	assert factorial(0) == 1
	assert factorial(1) == 1
	assert factorial(5) == 120
	assert factorial(7) == 5040

	try:
		factorial(-1)
	except ValueError:
		pass
	else:
		raise AssertionError("A negative number should raise ValueError")

	try:
		factorial(3.5)
	except TypeError:
		pass
	else:
		raise AssertionError("A non-integer should raise TypeError")


def run_calculator():
	print("Simple Calculator (+, -, *, /)")
	try:
		first = float(input("Enter the first number: "))
		operator = input("Enter an operation: ")
		second = float(input("Enter the second number: "))
		print("Result:", calculate(first, operator, second))
	except (ValueError, ZeroDivisionError) as error:
		print("Error:", error)


if __name__ == "__main__":
	run_assert_tests()
	print("All assertion tests passed.")
	run_calculator()

