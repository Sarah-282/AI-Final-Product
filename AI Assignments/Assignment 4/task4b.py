def count_vowels(text):
	"""Return the number of vowels in text, ignoring letter case."""
	vowels = "aeiou"
	return sum(1 for character in text.lower() if character in vowels)


test_strings = ["Hello", "Python", "Education"]

for text in test_strings:
	print(f'Input: "{text}"')
	print(f"Output: {count_vowels(text)}")
