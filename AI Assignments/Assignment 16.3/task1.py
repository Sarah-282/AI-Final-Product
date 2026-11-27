import sqlite3


connection = sqlite3.connect(":memory:")
connection.execute("PRAGMA foreign_keys = ON")

connection.executescript(
    """
    CREATE TABLE Doctors (
        doctor_id INTEGER PRIMARY KEY,
        full_name TEXT NOT NULL,
        specialty TEXT NOT NULL,
        license_number TEXT NOT NULL UNIQUE
    );

    CREATE TABLE Patients (
        patient_id INTEGER PRIMARY KEY,
        full_name TEXT NOT NULL,
        date_of_birth TEXT NOT NULL
            CHECK (date(date_of_birth) IS NOT NULL),
        phone TEXT
    );

    CREATE TABLE Appointments (
        appointment_id INTEGER PRIMARY KEY,
        doctor_id INTEGER NOT NULL,
        patient_id INTEGER NOT NULL,
        appointment_datetime TEXT NOT NULL
            CHECK (datetime(appointment_datetime) IS NOT NULL),
        diagnosis TEXT,
        status TEXT NOT NULL DEFAULT 'scheduled'
            CHECK (status IN ('scheduled', 'completed', 'cancelled')),
        FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id),
        FOREIGN KEY (patient_id) REFERENCES Patients(patient_id)
    );

    INSERT INTO Doctors VALUES
        (1, 'Maya Chen', 'Cardiology', 'MED-1001'),
        (2, 'Omar Patel', 'Pediatrics', 'MED-1002'),
        (3, 'Elena Ruiz', 'Neurology', 'MED-1003');

    INSERT INTO Patients VALUES
        (101, 'Ava Johnson', '1990-04-12', '555-0101'),
        (102, 'Noah Williams', '1985-09-23', '555-0102'),
        (103, 'Mia Davis', '2014-06-08', '555-0103'),
        (104, 'Liam Brown', '1978-12-30', '555-0104');

    INSERT INTO Appointments VALUES
        (1001, 1, 101, '2026-03-01 09:00:00', 'Hypertension', 'completed'),
        (1002, 1, 102, '2026-03-02 10:00:00', 'ECG review', 'completed'),
        (1003, 2, 101, '2026-03-04 11:00:00', 'Annual checkup', 'completed'),
        (1004, 2, 103, '2026-03-05 13:00:00', NULL, 'scheduled'),
        (1005, 3, 104, '2026-03-06 14:30:00', 'Migraine', 'completed');
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
    "Appointments by Doctor ID 1",
    connection.execute(
        """
        SELECT
            a.appointment_id,
            a.appointment_datetime,
            p.full_name AS patient_name,
            a.diagnosis,
            a.status
        FROM Appointments AS a
        JOIN Patients AS p ON p.patient_id = a.patient_id
        WHERE a.doctor_id = ?
        ORDER BY a.appointment_datetime
        """,
        (1,),
    ),
)

print_rows(
    "Patient History for Patient ID 101",
    connection.execute(
        """
        SELECT
            a.appointment_id,
            a.appointment_datetime,
            d.full_name AS doctor_name,
            d.specialty,
            a.diagnosis,
            a.status
        FROM Appointments AS a
        JOIN Doctors AS d ON d.doctor_id = a.doctor_id
        WHERE a.patient_id = ?
        ORDER BY a.appointment_datetime DESC
        """,
        (101,),
    ),
)

print_rows(
    "Distinct Patients Treated by Each Doctor",
    connection.execute(
        """
        SELECT
            d.doctor_id,
            d.full_name AS doctor_name,
            COUNT(DISTINCT CASE
                WHEN a.status = 'completed' THEN a.patient_id
            END) AS patients_treated
        FROM Doctors AS d
        LEFT JOIN Appointments AS a ON a.doctor_id = d.doctor_id
        GROUP BY d.doctor_id, d.full_name
        ORDER BY d.doctor_id
        """
    ),
)

connection.close()
