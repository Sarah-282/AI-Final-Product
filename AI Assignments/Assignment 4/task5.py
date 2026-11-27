def count_lines(filename):
	"""Return the number of lines in a text file."""
	# The with statement opens the file and closes it automatically.
	with open(filename, "r", encoding="utf-8") as file:
		return sum(1 for _ in file)


# Sample usage:
# If example1.txt contains:
# Hello
# World
# print(count_lines("example1.txt"))  # Output: 2 lines
#
# If example2.txt contains:
# Python
# is
# easy
# print(count_lines("example2.txt"))  # Output: 3 lines
#
# If example3.txt contains:
# AI
# print(count_lines("example3.txt"))  # Output: 1 line
