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


def main():
	run_assert_tests()
	print("All assertion tests passed.")
	try:
		number = int(input("Enter a non-negative integer: "))
		print(f"{number}! = {factorial(number)}")
	except ValueError as error:
		print("Error:", error)


if __name__ == "__main__":
	main()



