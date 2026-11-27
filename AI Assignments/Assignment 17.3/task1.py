import csv
import sys
from pathlib import Path
from statistics import median

employees = [
    {"ID": 101, "Name": "Alice", "Age": 25, "Department": "IT",
     "Job_Title": "Data Analyst", "Gender": "F", "Salary": 70000},
    {"ID": 102, "Name": "Bob", "Age": None, "Department": "HR",
     "Job_Title": "HR Manager", "Gender": "M", "Salary": 60000},
    {"ID": 103, "Name": "Robert", "Age": 31, "Department": "IT",
     "Job_Title": "Data Scientist", "Gender": "M", "Salary": 80000},
    {"ID": 103, "Name": "Cara", "Age": 40, "Department": None,
     "Job_Title": "Engineer", "Gender": "F", "Salary": None},
    {"ID": 104, "Name": "Dan", "Age": 28, "Department": "Sales",
     "Job_Title": None, "Gender": None, "Salary": 55000},
]

# Remove duplicate IDs, keeping the first record.
cleaned = []
seen_ids = set()
for employee in employees:
    if employee["ID"] not in seen_ids:
        cleaned.append(employee.copy())
        seen_ids.add(employee["ID"])

# Fill missing numeric values with each column's median.
numeric_columns = ("Age", "Salary")
for column in numeric_columns:
    column_median = median(
        row[column] for row in cleaned if row[column] is not None
    )
    for row in cleaned:
        if row[column] is None:
            row[column] = column_median

# Fill missing categories and lowercase job titles.
categorical_columns = ("Department", "Job_Title", "Gender")
for row in cleaned:
    for column in categorical_columns:
        if row[column] is None:
            row[column] = "Unknown"
    row["Job_Title"] = row["Job_Title"].lower()

# One-hot encode the categorical columns.
categories = {
    column: sorted({row[column] for row in cleaned})
    for column in categorical_columns
}
fieldnames = ["ID", "Name", "Age", "Salary"]
for column in categorical_columns:
    fieldnames.extend(f"{column}_{value}" for value in categories[column])

encoded = []
for row in cleaned:
    encoded_row = {column: row[column] for column in fieldnames[:4]}
    for column in categorical_columns:
        for value in categories[column]:
            encoded_row[f"{column}_{value}"] = int(row[column] == value)
    encoded.append(encoded_row)

# Print the result and save a CSV beside this script.
writer = csv.writer(sys.stdout, delimiter="\t", lineterminator="\n")
writer.writerow(fieldnames)
for row in encoded:
    writer.writerow(row[field] for field in fieldnames)

output_path = Path(__file__).with_name("cleaned_employees.csv")
with output_path.open("w", newline="", encoding="utf-8") as output_file:
    csv_writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    csv_writer.writeheader()
    csv_writer.writerows(encoded)

print(f"\nSaved cleaned data to: {output_path}")
