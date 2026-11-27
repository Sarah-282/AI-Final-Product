def is_leap_year(year):
	"""Return True if year is a leap year; otherwise return False."""
	# A year is a leap year when it is divisible by 400,
	# or divisible by 4 but not divisible by 100.
	return year % 400 == 0 or (year % 4 == 0 and year % 100 != 0)


test_years = [2024, 1900, 2000, 2023]

for year in test_years:
	result = "a leap year" if is_leap_year(year) else "not a leap year"
	print(f"{year} is {result}.")