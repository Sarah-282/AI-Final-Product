def is_armstrong(number):
	"""Return True if number equals the sum of its digits raised to a power.

	For a number with n digits, an Armstrong number satisfies:
	number = digit_1**n + digit_2**n + ... + digit_n**n
	"""
	if number < 0:
		return False

	digits = str(number)
	power = len(digits)
	digit_sum = sum(int(digit) ** power for digit in digits)

	return digit_sum == number


# 153 is Armstrong because 1**3 + 5**3 + 3**3 equals 153.
test_numbers = [0, 153, 9474, 123]

for number in test_numbers:
	result = "an Armstrong number" if is_armstrong(number) else "not an Armstrong number"
	print(f"{number} is {result}.")
