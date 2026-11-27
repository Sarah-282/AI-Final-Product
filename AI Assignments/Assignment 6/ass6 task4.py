def check_discount(age, is_member):
	if age >= 60:
		if is_member:
			return "Senior discount and additional member discount"
		else:
			return "Senior discount"
	else:
		if is_member:
			return "Additional member discount"
		else:
			return "No discount"


test_cases = [(65, True), (65, False), (30, True), (30, False)]

for age, is_member in test_cases:
	print(f"Age: {age}, Member: {is_member} -> {check_discount(age, is_member)}")
