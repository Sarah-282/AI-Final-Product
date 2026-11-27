import csv
import sys
from collections import Counter
from math import ceil
from pathlib import Path
from random import Random
from statistics import median, pstdev


students = [
    {"Student_ID": "S01", "Age": 18, "BMI": 21.5, "Sleep_Hours": 7.5,
     "Gender": "Female", "Activity_Level": "High", "Health_Status": "Healthy"},
    {"Student_ID": "S02", "Age": 19, "BMI": 27.1, "Sleep_Hours": 6.0,
     "Gender": "Male", "Activity_Level": "Low", "Health_Status": "At_Risk"},
    {"Student_ID": "S03", "Age": None, "BMI": 23.8, "Sleep_Hours": 8.0,
     "Gender": "Female", "Activity_Level": "Moderate", "Health_Status": "Healthy"},
    {"Student_ID": "S04", "Age": 20, "BMI": 31.2, "Sleep_Hours": 5.5,
     "Gender": "Male", "Activity_Level": "Low", "Health_Status": "At_Risk"},
    {"Student_ID": "S05", "Age": 21, "BMI": 24.1, "Sleep_Hours": 7.0,
     "Gender": "Female", "Activity_Level": None, "Health_Status": "Healthy"},
    {"Student_ID": "S06", "Age": 22, "BMI": 28.5, "Sleep_Hours": None,
     "Gender": "Male", "Activity_Level": "Moderate", "Health_Status": "At_Risk"},
    {"Student_ID": "S07", "Age": 18, "BMI": 22.0, "Sleep_Hours": 8.5,
     "Gender": None, "Activity_Level": "High", "Health_Status": "Healthy"},
    {"Student_ID": "S08", "Age": 20, "BMI": 30.0, "Sleep_Hours": 6.0,
     "Gender": "Male", "Activity_Level": "Low", "Health_Status": "At_Risk"},
]

numeric_columns = ("Age", "BMI", "Sleep_Hours")
categorical_columns = ("Gender", "Activity_Level")
target_mapping = {"Healthy": 0, "At_Risk": 1}

# Split first so imputers and scaling statistics are learned from training data only.
indices = list(range(len(students)))
Random(42).shuffle(indices)
test_count = ceil(len(students) * 0.25)
test_indices = indices[:test_count]
train_indices = indices[test_count:]

processed = [student.copy() for student in students]

# Impute numeric values with training medians.
for column in numeric_columns:
    fill_value = median(
        processed[index][column]
        for index in train_indices
        if processed[index][column] is not None
    )
    for row in processed:
        if row[column] is None:
            row[column] = fill_value

# Impute categorical values with training modes.
for column in categorical_columns:
    training_values = [
        processed[index][column]
        for index in train_indices
        if processed[index][column] is not None
    ]
    counts = Counter(training_values)
    fill_value = max(counts, key=counts.get)
    for row in processed:
        if row[column] is None:
            row[column] = fill_value

# One-hot encode categories found in the training data.
categories = {
    column: sorted({processed[index][column] for index in train_indices})
    for column in categorical_columns
}
feature_columns = list(numeric_columns)
for column in categorical_columns:
    feature_columns.extend(
        f"{column}_{category}" for category in categories[column]
    )

# StandardScaler-equivalent transformation: (value - training mean) / training SD.
means = {
    column: sum(processed[index][column] for index in train_indices)
    / len(train_indices)
    for column in numeric_columns
}
scales = {}
for column in numeric_columns:
    values = [processed[index][column] for index in train_indices]
    standard_deviation = pstdev(values)
    scales[column] = standard_deviation if standard_deviation else 1.0

encoded = {}
for index, row in enumerate(processed):
    features = {
        column: (row[column] - means[column]) / scales[column]
        for column in numeric_columns
    }
    for column in categorical_columns:
        for category in categories[column]:
            features[f"{column}_{category}"] = int(row[column] == category)
    encoded[index] = {
        "Student_ID": row["Student_ID"],
        **features,
        "Health_Status": target_mapping[row["Health_Status"]],
    }


def print_split(title, split_indices):
    print(f"\n{title}")
    writer = csv.writer(sys.stdout, delimiter="\t", lineterminator="\n")
    writer.writerow(["Student_ID", *feature_columns, "Health_Status"])
    for index in split_indices:
        row = encoded[index]
        writer.writerow([
            row["Student_ID"],
            *(f'{row[column]:.3f}' if column in numeric_columns
              else row[column] for column in feature_columns),
            row["Health_Status"],
        ])


print_split("Training data", train_indices)
print_split("Testing data", test_indices)

output_path = Path(__file__).with_name("preprocessed_student_health.csv")
with output_path.open("w", newline="", encoding="utf-8") as output_file:
    fields = ["Split", "Student_ID", *feature_columns, "Health_Status"]
    writer = csv.DictWriter(output_file, fieldnames=fields)
    writer.writeheader()
    for split_name, split_indices in (
        ("train", train_indices),
        ("test", test_indices),
    ):
        for index in split_indices:
            writer.writerow({
                "Split": split_name,
                **encoded[index],
            })

print(f"\nSaved preprocessed data to: {output_path}")
