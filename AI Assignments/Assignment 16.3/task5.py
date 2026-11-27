import sqlite3


connection = sqlite3.connect(":memory:")
connection.execute("PRAGMA foreign_keys = ON")

connection.executescript(
    """
    CREATE TABLE Students (
        student_id INTEGER PRIMARY KEY,
        full_name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        major TEXT NOT NULL,
        CHECK (length(trim(full_name)) > 0),
        CHECK (instr(email, '@') > 1)
    );

    CREATE TABLE Faculty (
        faculty_id INTEGER PRIMARY KEY,
        full_name TEXT NOT NULL,
        department TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        CHECK (length(trim(full_name)) > 0),
        CHECK (instr(email, '@') > 1)
    );

    CREATE TABLE Courses (
        course_id INTEGER PRIMARY KEY,
        course_code TEXT NOT NULL UNIQUE,
        course_name TEXT NOT NULL,
        credits INTEGER NOT NULL,
        faculty_id INTEGER NOT NULL,
        FOREIGN KEY (faculty_id) REFERENCES Faculty(faculty_id),
        CHECK (credits BETWEEN 1 AND 6),
        CHECK (length(trim(course_name)) > 0)
    );

    CREATE TABLE Registrations (
        student_id INTEGER NOT NULL,
        course_id INTEGER NOT NULL,
        registration_date TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'registered',
        PRIMARY KEY (student_id, course_id),
        FOREIGN KEY (student_id) REFERENCES Students(student_id),
        FOREIGN KEY (course_id) REFERENCES Courses(course_id),
        CHECK (date(registration_date) IS NOT NULL),
        CHECK (status IN ('registered', 'waitlisted', 'dropped'))
    );

    CREATE INDEX idx_courses_faculty ON Courses(faculty_id);
    CREATE INDEX idx_registrations_course ON Registrations(course_id);
    CREATE INDEX idx_registrations_student ON Registrations(student_id);

    INSERT INTO Students (student_id, full_name, email, major) VALUES
        (1001, 'Aarav Shah', 'aarav@sr.edu', 'Computer Science'),
        (1002, 'Sara Khan', 'sara@sr.edu', 'Data Science'),
        (1003, 'Leo Martin', 'leo@sr.edu', 'Electronics'),
        (1004, 'Mia Davis', 'mia@sr.edu', 'Computer Science');

    INSERT INTO Faculty (faculty_id, full_name, department, email) VALUES
        (201, 'Dr. Maya Chen', 'Computer Science', 'maya.chen@sr.edu'),
        (202, 'Dr. Omar Patel', 'Mathematics', 'omar.patel@sr.edu'),
        (203, 'Dr. Elena Ruiz', 'Electronics', 'elena.ruiz@sr.edu');

    INSERT INTO Courses (
        course_id, course_code, course_name, credits, faculty_id
    ) VALUES
        (301, 'CS101', 'Programming Fundamentals', 4, 201),
        (302, 'CS201', 'Database Systems', 4, 201),
        (303, 'CS301', 'Algorithms', 3, 201),
        (304, 'MA201', 'Discrete Mathematics', 3, 202),
        (305, 'EC201', 'Digital Circuits', 3, 203);

    INSERT INTO Registrations (
        student_id, course_id, registration_date, status
    ) VALUES
        (1001, 301, '2026-07-01', 'registered'),
        (1001, 302, '2026-07-01', 'registered'),
        (1002, 301, '2026-07-02', 'registered'),
        (1002, 304, '2026-07-02', 'registered'),
        (1003, 301, '2026-07-03', 'registered'),
        (1003, 305, '2026-07-03', 'registered'),
        (1004, 301, '2026-07-04', 'registered'),
        (1004, 302, '2026-07-04', 'registered'),
        (1004, 303, '2026-07-04', 'waitlisted');
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
    "Students Registered in CS101",
    connection.execute(
        """
        SELECT
            s.student_id,
            s.full_name,
            s.major,
            r.status,
            r.registration_date
        FROM Registrations AS r
        JOIN Students AS s ON s.student_id = r.student_id
        JOIN Courses AS c ON c.course_id = r.course_id
        WHERE c.course_code = ?
          AND r.status <> 'dropped'
        ORDER BY s.full_name
        """,
        ("CS101",),
    ),
)

print_rows(
    "Faculty Teaching More Than 2 Courses",
    connection.execute(
        """
        SELECT
            f.faculty_id,
            f.full_name,
            f.department,
            COUNT(c.course_id) AS course_count
        FROM Faculty AS f
        JOIN Courses AS c ON c.faculty_id = f.faculty_id
        GROUP BY f.faculty_id, f.full_name, f.department
        HAVING COUNT(c.course_id) > 2
        ORDER BY course_count DESC, f.full_name
        """
    ),
)

print_rows(
    "Course(s) with the Highest Registrations",
    connection.execute(
        """
        WITH RegistrationCounts AS (
            SELECT
                c.course_id,
                c.course_code,
                c.course_name,
                COUNT(r.student_id) AS registration_count
            FROM Courses AS c
            LEFT JOIN Registrations AS r
              ON r.course_id = c.course_id
             AND r.status <> 'dropped'
            GROUP BY c.course_id, c.course_code, c.course_name
        )
        SELECT course_id, course_code, course_name, registration_count
        FROM RegistrationCounts
        WHERE registration_count = (
            SELECT MAX(registration_count)
            FROM RegistrationCounts
        )
        ORDER BY course_code
        """
    ),
)

print(
    """
\nRelationships
- Faculty 1-to-many Courses: Faculty.faculty_id -> Courses.faculty_id.
- Students many-to-many Courses: represented by Registrations.
- Registrations uses (student_id, course_id) as its composite primary key.

Indexes
- idx_courses_faculty supports faculty-course lookups.
- idx_registrations_course supports student-list and registration-count queries.
- idx_registrations_student supports each student's course history.
"""
)

connection.close()
