def cm_to_inches(centimeters):
	"""Convert centimeters to inches using 1 inch = 2.54 centimeters."""
	return centimeters / 2.54


test_values = [10, 2.54, 25.4]

for centimeters in test_values:
	inches = cm_to_inches(centimeters)
	print(f"Input: {centimeters} cm")
	print(f"Output: {inches:.2f} inches")
