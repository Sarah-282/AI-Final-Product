def format_name(full_name):
	"""Format a two-part name as 'Last, First'."""
	parts = full_name.strip().split()

	if len(parts) != 2:
		raise ValueError("Please enter a first name and a last name.")

	first_name, last_name = parts
	return f"{last_name}, {first_name}"


sample_names = ["John Smith", "Anita Rao", "David Kumar"]

for name in sample_names:
	print(f'Input: "{name}"')
	print(f'Output: "{format_name(name)}"')
