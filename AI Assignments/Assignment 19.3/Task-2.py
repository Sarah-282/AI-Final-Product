def is_prime(number: int) -> bool:
    """Return whether number is a prime integer."""
    if number < 2:
        return False
    if number == 2:
        return True
    if number % 2 == 0:
        return False

    divisor = 3
    while divisor * divisor <= number:
        if number % divisor == 0:
            return False
        divisor += 2
    return True


if __name__ == "__main__":
    test_cases = {
        -3: False,
        0: False,
        1: False,
        2: True,
        3: True,
        4: False,
        17: True,
        25: False,
        97: True,
        100: False,
    }

    for value, expected in test_cases.items():
        result = is_prime(value)
        assert result == expected, f"is_prime({value}) returned {result}"
        print(f"is_prime({value}) = {result}")
