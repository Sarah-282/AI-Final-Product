# Task 5: Bubble Sort Translation (Python and JavaScript)

Both programs implement bubble sort: compare adjacent values, swap them when
they are out of order, and stop early if a pass makes no swaps. Each function
sorts a copy, leaving its input unchanged.

## Translation notes

- Python uses `range`, `len`, and tuple assignment; JavaScript uses indexed
  `for` loops, `.length`, and array destructuring for swaps.
- Both implementations use only language built-ins; no extra libraries are
  required.
- Both runtimes manage memory automatically. Each function creates a copy of
  the input array/list, so it uses additional O(n) space.
- JavaScript `Number` cannot precisely represent every arbitrarily large
  integer, unlike Python's `int`. These examples use ordinary safe integer
  values.

## Run and test

From the project directory in PowerShell:

```powershell
python .\Task5.py
node .\Task5.js
```

Each program tests the same five inputs (including empty, duplicate, and
negative values) against expected sorted results.
