def print_triangle_for(rows):
	for row in range(1, rows + 1):
		print("*" * row)


def print_triangle_while(rows):
	row = 1
	while row <= rows:
		print("*" * row)
		row += 1


rows = int(input("Enter the number of rows: "))

print("Using for loop:")
print_triangle_for(rows)

print("Using while loop:")
print_triangle_while(rows)
