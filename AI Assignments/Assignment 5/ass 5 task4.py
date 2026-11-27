def quick_sort(numbers):
	"""Return a sorted copy of numbers using QuickSort."""
	# A list with zero or one item is already sorted.
	if len(numbers) <= 1:
		return numbers.copy()

	# Choose the last item as the pivot.
	pivot = numbers[-1]

	# Divide the remaining items into two groups around the pivot.
	smaller = [number for number in numbers[:-1] if number <= pivot]
	larger = [number for number in numbers[:-1] if number > pivot]

	# Sort both groups recursively and place the pivot between them.
	return quick_sort(smaller) + [pivot] + quick_sort(larger)


def bubble_sort(numbers):
	"""Return a sorted copy of numbers using BubbleSort."""
	sorted_numbers = numbers.copy()

	# Make repeated passes through the list.
	for pass_number in range(len(sorted_numbers) - 1):
		swapped = False

		# Compare adjacent items and swap them when they are out of order.
		for index in range(len(sorted_numbers) - 1 - pass_number):
			if sorted_numbers[index] > sorted_numbers[index + 1]:
				sorted_numbers[index], sorted_numbers[index + 1] = (
					sorted_numbers[index + 1],
					sorted_numbers[index],
				)
				swapped = True

		# Stop early if this pass made no swaps.
		if not swapped:
			break

	return sorted_numbers


numbers = [64, 34, 25, 12, 22, 11, 90]
print("Original list:", numbers)
print("QuickSort result:", quick_sort(numbers))
print("BubbleSort result:", bubble_sort(numbers))

# Difference: QuickSort divides the list around a pivot and is usually faster
# for large lists, while BubbleSort repeatedly swaps adjacent items and is
# easier to understand but usually slower for large lists.
