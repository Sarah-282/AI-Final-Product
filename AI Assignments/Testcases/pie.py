import pytest


def calculate(a, operator, b):
	"""Return the result of a basic arithmetic operation."""
	if operator == "+":
		return a + b
	if operator == "-":
		return a - b
	if operator == "*":
		return a * b
	if operator == "/":
		if b == 0:
			raise ZeroDivisionError("Cannot divide by zero")
		return a / b
	raise ValueError(f"Unsupported operator: {operator}")


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
	"""Return True if number is prime, otherwise return False.

	Numbers less than 2 are not prime. Only integers are accepted.
	"""
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


def test_addition():
	assert calculate(2, "+", 3) == 5


def test_subtraction():
	assert calculate(5, "-", 3) == 2


def test_multiplication():
	assert calculate(2, "*", 3) == 6


def test_division():
	assert calculate(6, "/", 3) == 2


def test_division_by_zero():
	import pytest

	with pytest.raises(ZeroDivisionError):
		calculate(1, "/", 0)


def test_factorial_of_zero():
	assert factorial(0) == 1


def test_factorial_of_one():
	assert factorial(1) == 1


def test_factorial_of_positive_integer():
	assert factorial(5) == 120


def test_factorial_of_negative_integer():
	import pytest

	with pytest.raises(ValueError, match="number must be non-negative"):
		factorial(-1)


def test_factorial_rejects_non_integer():
	import pytest

	with pytest.raises(TypeError, match="number must be an integer"):
		factorial(3.5)


@pytest.mark.parametrize(
	"number, expected",
	[
		(-10, False),
		(-1, False),
		(0, False),
		(1, False),
		(2, True),
		(3, True),
		(4, False),
		(5, True),
		(9, False),
		(11, True),
		(15, False),
		(17, True),
		(25, False),
		(29, True),
		(49, False),
		(97, True),
		(100, False),
		(101, True),
	],
)
def test_is_prime_for_integer(number, expected):
	assert is_prime(number) is expected


def test_is_prime_rejects_float():
	with pytest.raises(TypeError, match="number must be an integer"):
		is_prime(2.5)


def test_is_prime_rejects_boolean():
	with pytest.raises(TypeError, match="number must be an integer"):
		is_prime(True)


