def count_vowels(text):
	"""Return the number of uppercase and lowercase vowels in text."""
	vowels = "aeiou"
	return sum(1 for character in text.lower() if character in vowels)


test_cases = ["Hello", "AEIOU", "Education"]

for text in test_cases:
	print(f'Input: "{text}"')
	print(f"Output: {count_vowels(text)}")
