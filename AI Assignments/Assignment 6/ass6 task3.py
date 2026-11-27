def check_number(number):
	if number > 0:
		return "positive"
	elif number < 0:
		return "negative"
	else:
		return "zero"


test_numbers = [-10, 0, 25]

for number in test_numbers:
	print(f"{number} is {check_number(number)}.")
