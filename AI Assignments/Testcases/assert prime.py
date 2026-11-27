def is_prime(number):
	"""Return True if number is prime; otherwise return False."""
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


def run_assert_tests():
	test_cases = (
		(-5, False),
		(-1, False),
		(0, False),
		(1, False),
		(2, True),
		(3, True),
		(4, False),
		(5, True),
		(9, False),
		(17, True),
		(25, False),
		(49, False),
		(97, True),
		(100, False),
		(101, True),
	)
	for number, expected in test_cases:
		assert is_prime(number) is expected, f"is_prime({number}) should be {expected}"

	for invalid_number in (2.5, True):
		try:
			is_prime(invalid_number)
		except TypeError:
			pass
		else:
			raise AssertionError("Non-integer inputs should raise TypeError")


if __name__ == "__main__":
	run_assert_tests()
	print("All prime-number assertion tests passed.")
	try:
		number = int(input("Enter an integer: "))
		if is_prime(number):
			print(f"{number} is prime.")
		else:
			print(f"{number} is not prime.")
	except ValueError:
		print("Error: please enter a valid integer.")
