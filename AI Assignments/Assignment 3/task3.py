def is_prime(number):
	"""Return True when number has exactly two positive factors."""
	# Numbers below 2 are not prime.
	if number < 2:
		return False

	# Only test divisors up to the square root of the number.
	divisor = 2
	while divisor * divisor <= number:
		if number % divisor == 0:
			return False
		divisor += 1

	return True


# Few-shot examples: these input-output pairs clarify expected behavior.
examples = {
	1: False,    # Less than 2: not prime
	2: True,     # Smallest prime number
	7: True,     # Prime number
	9: False,    # Divisible by 3: not prime
	25: False,   # Divisible by 5: not prime
	29: True,    # Larger prime number
}

for number, expected in examples.items():
	result = is_prime(number)
	print(f"Input: {number}, Output: {result}, Expected: {expected}")
