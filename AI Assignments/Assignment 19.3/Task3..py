def bubble_sort(numbers: list[int]) -> list[int]:
    """Return the numbers sorted in ascending order using bubble sort."""
    result = numbers.copy()

    for end in range(len(result) - 1, 0, -1):
        swapped = False
        for index in range(end):
            if result[index] > result[index + 1]:
                result[index], result[index + 1] = result[index + 1], result[index]
                swapped = True
        if not swapped:
            break

    return result


if __name__ == "__main__":
    test_cases = [
        ([5, 1, 4, 2, 8], [1, 2, 4, 5, 8]),
        ([], []),
        ([7], [7]),
        ([3, 3, 1, 2, 1], [1, 1, 2, 3, 3]),
        ([-2, 5, 0, -7], [-7, -2, 0, 5]),
    ]

    for values, expected in test_cases:
        result = bubble_sort(values)
        assert result == expected, f"bubble_sort({values}) returned {result}"
        print(f"{values} -> {result}")