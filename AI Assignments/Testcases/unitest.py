import unittest


def calculate(first, operator, second):
	"""Calculate using +, -, *, or /."""
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


def is_prime(number):
	"""Return whether number is a prime integer."""
	if not isinstance(number, int) or isinstance(number, bool):
		raise TypeError("number must be an integer")
	if number < 2:
		return False

	divisor = 2
	while divisor * divisor <= number:
		if number % divisor == 0:
			return False
		divisor += 1
	return True


class TestCalculate(unittest.TestCase):
	def test_addition(self):
		self.assertEqual(calculate(2, "+", 3), 5)

	def test_subtraction(self):
		self.assertEqual(calculate(5, "-", 3), 2)

	def test_multiplication(self):
		self.assertEqual(calculate(4, "*", 3), 12)

	def test_division(self):
		self.assertEqual(calculate(8, "/", 2), 4)

	def test_division_by_zero(self):
		with self.assertRaises(ZeroDivisionError):
			calculate(1, "/", 0)

	def test_unsupported_operator(self):
		with self.assertRaises(ValueError):
			calculate(2, "%", 3)



class TestFactorial(unittest.TestCase):
	def test_zero_factorial(self):
		self.assertEqual(factorial(0), 1)

	def test_one_factorial(self):
		self.assertEqual(factorial(1), 1)

	def test_positive_integer_factorial(self):
		self.assertEqual(factorial(5), 120)

	def test_larger_integer_factorial(self):
		self.assertEqual(factorial(7), 5040)

	def test_negative_input(self):
		with self.assertRaises(ValueError):
			factorial(-1)

	def test_non_integer_input(self):
		with self.assertRaises(TypeError):
			factorial(3.5)

	def test_boolean_input(self):
		with self.assertRaises(TypeError):
			factorial(True)


class TestPrime(unittest.TestCase):
	def test_prime_numbers(self):
		for number in (2, 3, 5, 97):
			with self.subTest(number=number):
				self.assertTrue(is_prime(number))

	def test_composite_numbers(self):
		for number in (4, 9, 25, 100):
			with self.subTest(number=number):
				self.assertFalse(is_prime(number))

	def test_numbers_less_than_two_are_not_prime(self):
		for number in (-7, 0, 1):
			with self.subTest(number=number):
				self.assertFalse(is_prime(number))

	def test_non_integer_input(self):
		with self.assertRaises(TypeError):
			is_prime(2.5)

	def test_boolean_input(self):
		with self.assertRaises(TypeError):
			is_prime(True)


def run_factorial():
	print("Factorial Calculator")
	try:
		number = int(input("Enter a non-negative integer: "))
		print(f"{number}! = {factorial(number)}")
	except ValueError as error:
		print("Error:", error)


def run_prime():
	print("Prime Number Checker")
	try:
		number = int(input("Enter an integer: "))
		if is_prime(number):
			print(f"{number} is prime.")
		else:
			print(f"{number} is not prime.")
	except ValueError:
		print("Error: please enter a valid integer.")


if __name__ == "__main__":
	run_prime()







