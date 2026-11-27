import sqlite3


connection = sqlite3.connect(":memory:")
connection.execute("PRAGMA foreign_keys = ON")

connection.executescript(
    """
    CREATE TABLE Books (
        book_id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        isbn TEXT NOT NULL UNIQUE,
        available_copies INTEGER NOT NULL DEFAULT 0
    );

    CREATE TABLE Members (
        member_id INTEGER PRIMARY KEY,
        full_name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        join_date TEXT NOT NULL
    );

    CREATE TABLE Loans (
        loan_id INTEGER PRIMARY KEY,
        book_id INTEGER NOT NULL,
        member_id INTEGER NOT NULL,
        loan_date TEXT NOT NULL,
        due_date TEXT NOT NULL,
        return_date TEXT,
        FOREIGN KEY (book_id) REFERENCES Books(book_id),
        FOREIGN KEY (member_id) REFERENCES Members(member_id)
    );

    INSERT INTO Books VALUES
        (101, 'The Alchemist', 'Paulo Coelho', '9780061122415', 2),
        (102, 'Clean Code', 'Robert C. Martin', '9780132350884', 1),
        (103, 'The Hobbit', 'J. R. R. Tolkien', '9780547928227', 3);

    INSERT INTO Members VALUES
        (1, 'Ava Johnson', 'ava@example.com', '2025-01-15'),
        (2, 'Noah Williams', 'noah@example.com', '2025-05-20'),
        (3, 'Mia Davis', 'mia@example.com', '2026-02-10');

    INSERT INTO Loans VALUES
        (1001, 101, 1, '2026-09-25', '2026-10-25', NULL),
        (1002, 102, 2, '2026-10-10', '2026-11-09', NULL),
        (1003, 103, 1, '2026-08-01', '2026-08-31', '2026-08-28');
    """
)

ORIGINAL_QUERY = """
    SELECT
        b.title,
        m.full_name AS member_name,
        l.loan_date,
        l.due_date
    FROM Loans AS l
    JOIN Books AS b ON b.book_id = l.book_id
    JOIN Members AS m ON m.member_id = l.member_id
    WHERE l.loan_id IN (
        SELECT loan_id
        FROM Loans
        WHERE return_date IS NULL
          AND due_date < date('now')
          AND julianday(date('now')) - julianday(loan_date) > 30
    )
    ORDER BY l.due_date
"""

OPTIMIZED_QUERY = """
    SELECT
        b.title,
        m.full_name AS member_name,
        l.loan_date,
        l.due_date
    FROM Loans AS l
    JOIN Books AS b ON b.book_id = l.book_id
    JOIN Members AS m ON m.member_id = l.member_id
    WHERE l.return_date IS NULL
      AND l.due_date < date('now')
      AND l.loan_date < date('now', '-30 days')
    ORDER BY l.due_date
"""


def print_query_plan(title, query):
    print(f"\n{title}")
    for row in connection.execute("EXPLAIN QUERY PLAN " + query):
        print(" | ".join(str(value) for value in row))


print("Sample date:", connection.execute("SELECT date('now')").fetchone()[0])

print("\nOriginal query results:")
original_rows = connection.execute(ORIGINAL_QUERY).fetchall()
for row in original_rows:
    print(row)

print("\nOptimized query results:")
optimized_rows = connection.execute(OPTIMIZED_QUERY).fetchall()
for row in optimized_rows:
    print(row)

print("\nResult comparison:",
      "SAME" if set(original_rows) == set(optimized_rows) else "DIFFERENT")

print("\nQuery plans before the added index:")
print_query_plan("Original", ORIGINAL_QUERY)
print_query_plan("Optimized", OPTIMIZED_QUERY)

connection.execute(
    "CREATE INDEX idx_loans_overdue "
    "ON Loans(return_date, due_date, loan_date)"
)

print("\nQuery plans after the added index:")
print_query_plan("Original", ORIGINAL_QUERY)
print_query_plan("Optimized", OPTIMIZED_QUERY)

print(
    """
\nExplanation
The IN subquery is unnecessary because loan_id is already the primary key.
Both queries return the same overdue, unreturned loans. The optimized version
applies the overdue predicates once, in the outer Loans table, and uses only
one pass over the relevant table.

The optimized predicate replaces the date arithmetic:
  julianday(date('now')) - julianday(loan_date) > 30
with:
  loan_date < date('now', '-30 days')

This second form is clearer and can use an index on loan_date. The composite
index idx_loans_overdue(return_date, due_date, loan_date) supports the two
record-level filters. Use ANALYZE and EXPLAIN QUERY PLAN with real data:
index effectiveness depends on table size and selectivity.
"""
)

connection.close()
