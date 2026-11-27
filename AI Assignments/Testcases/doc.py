"""A simple calculator with doctest examples.

Run the examples with ``python -m doctest -v doc.py``.
"""


def add(a, b):
	"""Return the sum of *a* and *b*.

	>>> add(2, 3)
	5
	>>> add(-1, 1)
	0
	"""
	return a + b


def subtract(a, b):
	"""Return *b* subtracted from *a*.

	>>> subtract(5, 3)
	2
	>>> subtract(3, 5)
	-2
	"""
	return a - b


def multiply(a, b):
	"""Return the product of *a* and *b*.

	>>> multiply(4, 3)
	12
	>>> multiply(-2, 3)
	-6
	"""
	return a * b


def divide(a, b):
	"""Return *a* divided by *b*.

	>>> divide(8, 2)
	4.0
	>>> divide(5, 2)
	2.5
	>>> divide(1, 0)
	Traceback (most recent call last):
	...
	ZeroDivisionError: Cannot divide by zero
	"""
	if b == 0:
		raise ZeroDivisionError("Cannot divide by zero")
	return a / b


def factorial(number):
	"""Return the factorial of a non-negative integer.

	>>> factorial(0)
	1
	>>> factorial(1)
	1
	>>> factorial(5)
	120
	>>> factorial(7)
	5040
	>>> factorial(-1)
	Traceback (most recent call last):
	...
	ValueError: number must be non-negative
	>>> factorial(2.5)
	Traceback (most recent call last):
	...
	TypeError: number must be an integer
	"""
	if not isinstance(number, int) or isinstance(number, bool):
		raise TypeError("number must be an integer")
	if number < 0:
		raise ValueError("number must be non-negative")

	result = 1
	for factor in range(2, number + 1):
		result *= factor
	return result


def is_prime(number):
	"""Return whether *number* is a prime integer.

	Numbers below 2 are not prime. A prime has no positive divisors other than
	1 and itself.

	>>> is_prime(-10)
	False
	>>> is_prime(-1)
	False
	>>> is_prime(0)
	False
	>>> is_prime(1)
	False
	>>> is_prime(2)
	True
	>>> is_prime(3)
	True
	>>> is_prime(4)
	False
	>>> is_prime(5)
	True
	>>> is_prime(9)
	False
	>>> is_prime(11)
	True
	>>> is_prime(15)
	False
	>>> is_prime(17)
	True
	>>> is_prime(25)
	False
	>>> is_prime(29)
	True
	>>> is_prime(49)
	False
	>>> is_prime(97)
	True
	>>> is_prime(100)
	False
	>>> is_prime(101)
	True
	>>> is_prime(True)
	Traceback (most recent call last):
	...
	TypeError: number must be an integer
	>>> is_prime(2.5)
	Traceback (most recent call last):
	...
	TypeError: number must be an integer
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


if __name__ == "__main__":
	import doctest

	doctest.testmod()


    


