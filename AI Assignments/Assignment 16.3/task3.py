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
        available_copies INTEGER NOT NULL DEFAULT 0,
        CHECK (length(trim(title)) > 0),
        CHECK (length(trim(author)) > 0),
        CHECK (length(trim(isbn)) > 0),
        CHECK (available_copies >= 0)
    );

    CREATE TABLE Members (
        member_id INTEGER PRIMARY KEY,
        full_name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        join_date TEXT NOT NULL,
        CHECK (length(trim(full_name)) > 0),
        CHECK (instr(email, '@') > 1),
        CHECK (date(join_date) IS NOT NULL)
    );

    CREATE TABLE Loans (
        loan_id INTEGER PRIMARY KEY,
        book_id INTEGER NOT NULL,
        member_id INTEGER NOT NULL,
        loan_date TEXT NOT NULL,
        due_date TEXT NOT NULL,
        return_date TEXT,
        FOREIGN KEY (book_id) REFERENCES Books(book_id),
        FOREIGN KEY (member_id) REFERENCES Members(member_id),
        CHECK (date(loan_date) IS NOT NULL),
        CHECK (date(due_date) IS NOT NULL),
        CHECK (return_date IS NULL OR date(return_date) IS NOT NULL),
        CHECK (due_date >= loan_date)
    );

    CREATE INDEX idx_loans_book ON Loans(book_id);
    CREATE INDEX idx_loans_member ON Loans(member_id);
    CREATE INDEX idx_loans_status_due ON Loans(return_date, due_date);

    INSERT INTO Books (book_id, title, author, isbn, available_copies) VALUES
        (101, 'The Alchemist', 'Paulo Coelho', '9780061122415', 2),
        (102, 'Clean Code', 'Robert C. Martin', '9780132350884', 1),
        (103, 'The Hobbit', 'J. R. R. Tolkien', '9780547928227', 3),
        (104, 'Database Systems', 'Ramez Elmasri', '9780133970777', 0);

    INSERT INTO Members (member_id, full_name, email, join_date) VALUES
        (1, 'Ava Johnson', 'ava@example.com', '2025-01-15'),
        (2, 'Noah Williams', 'noah@example.com', '2025-05-20'),
        (3, 'Mia Davis', 'mia@example.com', '2026-02-10');

    INSERT INTO Loans (
        loan_id, book_id, member_id, loan_date, due_date, return_date
    ) VALUES
        (1001, 101, 1, '2026-09-25', '2026-10-25', NULL),
        (1002, 102, 2, '2026-10-10', '2026-11-09', NULL),
        (1003, 103, 1, '2026-08-01', '2026-08-31', '2026-08-28'),
        (1004, 104, 3, '2026-11-01', '2026-12-01', NULL),
        (1005, 101, 2, '2026-06-10', '2026-07-10', '2026-07-08');
    """
)


def print_rows(title, cursor):
    print(f"\n{title}")
    columns = [description[0] for description in cursor.description]
    print(" | ".join(columns))
    print("-" * (sum(len(column) for column in columns) + 3 * (len(columns) - 1)))
    for row in cursor.fetchall():
        print(" | ".join("" if value is None else str(value) for value in row))


print_rows(
    "Currently Issued Books",
    connection.execute(
        """
        SELECT
            l.loan_id,
            b.book_id,
            b.title,
            m.member_id,
            m.full_name AS member_name,
            l.loan_date,
            l.due_date
        FROM Loans AS l
        JOIN Books AS b ON b.book_id = l.book_id
        JOIN Members AS m ON m.member_id = l.member_id
        WHERE l.return_date IS NULL
        ORDER BY l.due_date, l.loan_id
        """
    ),
)

print_rows(
    "Overdue Books",
    connection.execute(
        """
        SELECT
            l.loan_id,
            b.title,
            m.full_name AS member_name,
            l.loan_date,
            l.due_date,
            CAST(julianday(date('now')) - julianday(l.due_date) AS INTEGER)
                AS days_overdue
        FROM Loans AS l
        JOIN Books AS b ON b.book_id = l.book_id
        JOIN Members AS m ON m.member_id = l.member_id
        WHERE l.return_date IS NULL
          AND l.due_date < date('now')
          AND julianday(date('now')) - julianday(l.loan_date) > 30
        ORDER BY l.due_date
        """
    ),
)

print_rows(
    "Books Loaned by Each Member",
    connection.execute(
        """
        SELECT
            m.member_id,
            m.full_name AS member_name,
            COUNT(l.loan_id) AS loan_count,
            COUNT(DISTINCT l.book_id) AS distinct_books
        FROM Members AS m
        LEFT JOIN Loans AS l ON l.member_id = m.member_id
        GROUP BY m.member_id, m.full_name
        ORDER BY m.member_id
        """
    ),
)

print(
    """
\nNormalization
- 1NF: all fields contain atomic values.
- 2NF: member and book details are stored separately from loan records.
- 3NF: no member or book attribute is repeated in Loans.
- A loan row is a many-to-many relationship record between Members and Books.

Indexes
- idx_loans_book: faster joins and lookups by book.
- idx_loans_member: faster member history queries.
- idx_loans_status_due: faster filtering of unreturned or overdue loans.
"""
)

connection.close()
