def convert_distance(value, from_unit, to_unit):
	"""Convert a non-negative distance between kilometers and miles.

	Supported units are "km" and "miles". The conversion factors are:
	1 kilometer = 0.621371 miles
	1 mile = 1.60934 kilometers
	"""
	from_unit = from_unit.lower()
	to_unit = to_unit.lower()

	if value < 0:
		raise ValueError("Distance cannot be negative.")
	if from_unit not in {"km", "miles"} or to_unit not in {"km", "miles"}:
		raise ValueError("Units must be 'km' or 'miles'.")

	if from_unit == to_unit:
		return value
	if from_unit == "km":
		return value * 0.621371
	return value * 1.60934


# Clear examples for both supported conversion directions.
kilometers_to_miles = convert_distance(10, "km", "miles")
miles_to_kilometers = convert_distance(10, "miles", "km")

print(f"10 km = {kilometers_to_miles:.2f} miles")
print(f"10 miles = {miles_to_kilometers:.2f} km")
