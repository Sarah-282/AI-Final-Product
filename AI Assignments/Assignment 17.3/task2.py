import csv
import sys
from datetime import datetime
from pathlib import Path


students = [
    {"Student_ID": "S101", "Exam_Date": "2025-01-15", "Marks": 78},
    {"Student_ID": "S102", "Exam_Date": "20/04/2025", "Marks": 92},
    {"Student_ID": "S103", "Exam_Date": "2025-07-10", "Marks": 65},
    {"Student_ID": "S104", "Exam_Date": "05-10-2025", "Marks": 88},
    {"Student_ID": "S105", "Exam_Date": "2025-12-11", "Marks": 100},
    {"Student_ID": "S106", "Exam_Date": "02/06/2025", "Marks": 5},
]


def parse_exam_date(value):
    for date_format in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            return datetime.strptime(value, date_format).date()
        except ValueError:
            pass
    raise ValueError(f"Unsupported exam date: {value}")


def percentile(sorted_values, fraction):
    position = (len(sorted_values) - 1) * fraction
    lower_index = int(position)
    upper_index = min(lower_index + 1, len(sorted_values) - 1)
    weight = position - lower_index
    return (
        sorted_values[lower_index] * (1 - weight)
        + sorted_values[upper_index] * weight
    )


# Convert dates, extract month/semester, and sort marks for IQR calculation.
marks_sorted = sorted(student["Marks"] for student in students)
q1 = percentile(marks_sorted, 0.25)
q3 = percentile(marks_sorted, 0.75)
iqr = q3 - q1
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

processed = []
for student in students:
    exam_date = parse_exam_date(student["Exam_Date"])
    month = exam_date.month
    adjusted_marks = min(max(student["Marks"], lower_bound), upper_bound)
    processed.append({
        "Student_ID": student["Student_ID"],
        "Exam_Date": exam_date.isoformat(),
        "Month": month,
        "Semester": 1 if month <= 6 else 2,
        "Marks_IQR": adjusted_marks,
    })

# Min-max normalize the IQR-adjusted marks to the range 0-1.
minimum = min(row["Marks_IQR"] for row in processed)
maximum = max(row["Marks_IQR"] for row in processed)
for row in processed:
    if maximum == minimum:
        row["Normalized_Marks"] = 0.0
    else:
        row["Normalized_Marks"] = (
            (row["Marks_IQR"] - minimum) / (maximum - minimum)
        )

fieldnames = [
    "Student_ID", "Exam_Date", "Month", "Semester",
    "Marks_IQR", "Normalized_Marks",
]

print(f"IQR bounds: {lower_bound:.3f} to {upper_bound:.3f}")
writer = csv.writer(sys.stdout, delimiter="\t", lineterminator="\n")
writer.writerow(fieldnames)
for row in processed:
    writer.writerow([
        row["Student_ID"],
        row["Exam_Date"],
        row["Month"],
        row["Semester"],
        f'{row["Marks_IQR"]:.3f}',
        f'{row["Normalized_Marks"]:.3f}',
    ])

output_path = Path(__file__).with_name("cleaned_students.csv")
with output_path.open("w", newline="", encoding="utf-8") as output_file:
    csv_writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    csv_writer.writeheader()
    csv_writer.writerows(processed)

print(f"\nSaved cleaned data to: {output_path}")
