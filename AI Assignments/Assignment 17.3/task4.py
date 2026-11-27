import csv
import sys
from pathlib import Path
from statistics import median


rides = [
    {"Ride_ID": "R001", "Pickup_Location": " new york ",
     "Dropoff_Location": "brooklyn", "Fare": 25.0, "Driver_Rating": 4.8},
    {"Ride_ID": "R002", "Pickup_Location": "NEW YORK",
     "Dropoff_Location": " Queens ", "Fare": None, "Driver_Rating": 4.2},
    {"Ride_ID": "R003", "Pickup_Location": " CHICAGO ",
     "Dropoff_Location": "evanston", "Fare": 18.5, "Driver_Rating": 3.9},
    {"Ride_ID": "R003", "Pickup_Location": "Chicago",
     "Dropoff_Location": "Evanston", "Fare": 21.0, "Driver_Rating": 4.1},
    {"Ride_ID": "R004", "Pickup_Location": "los angeles",
     "Dropoff_Location": " SANTA MONICA ", "Fare": 32.0, "Driver_Rating": 5.0},
    {"Ride_ID": "R005", "Pickup_Location": "New York ",
     "Dropoff_Location": "BROOKLYN", "Fare": 21.0, "Driver_Rating": 4.0},
]


def standardize_location(location):
    return " ".join(location.split()).title()


# Standardize location text before removing duplicate ride IDs.
for ride in rides:
    ride["Pickup_Location"] = standardize_location(ride["Pickup_Location"])
    ride["Dropoff_Location"] = standardize_location(ride["Dropoff_Location"])

# Keep the first record for each ride ID.
cleaned = []
seen_ids = set()
for ride in rides:
    if ride["Ride_ID"] not in seen_ids:
        cleaned.append(ride.copy())
        seen_ids.add(ride["Ride_ID"])

# Fill missing fares with the median of the remaining rides.
fare_median = median(
    ride["Fare"] for ride in cleaned if ride["Fare"] is not None
)
for ride in cleaned:
    if ride["Fare"] is None:
        ride["Fare"] = fare_median

# Min-max normalize driver ratings to 0-1.
minimum_rating = min(ride["Driver_Rating"] for ride in cleaned)
maximum_rating = max(ride["Driver_Rating"] for ride in cleaned)
for ride in cleaned:
    if maximum_rating == minimum_rating:
        ride["Normalized_Rating"] = 0.0
    else:
        ride["Normalized_Rating"] = (
            (ride["Driver_Rating"] - minimum_rating)
            / (maximum_rating - minimum_rating)
        )

fields = [
    "Ride_ID", "Pickup_Location", "Dropoff_Location", "Fare",
    "Driver_Rating", "Normalized_Rating",
]

writer = csv.writer(sys.stdout, delimiter="\t", lineterminator="\n")
writer.writerow(fields)
for ride in cleaned:
    writer.writerow([
        ride["Ride_ID"],
        ride["Pickup_Location"],
        ride["Dropoff_Location"],
        f'{ride["Fare"]:.2f}',
        f'{ride["Driver_Rating"]:.2f}',
        f'{ride["Normalized_Rating"]:.3f}',
    ])

output_path = Path(__file__).with_name("cleaned_rides.csv")
with output_path.open("w", newline="", encoding="utf-8") as output_file:
    csv_writer = csv.DictWriter(output_file, fieldnames=fields)
    csv_writer.writeheader()
    csv_writer.writerows(cleaned)

print(f"\nSaved cleaned data to: {output_path}")
