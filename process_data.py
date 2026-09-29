# /// script
# requires-python = ">=3.10"
# ///

import csv
from pathlib import Path
from collections import defaultdict
from statistics import mean, pstdev


ROOT = Path(__file__).parent

INPUT_FILE = ROOT / "data" / "POWER_Regional_Monthly_2016_2025.csv"
OUTPUT_FILE = ROOT / "data" / "solar_summary_2016_2025.csv"


def read_nasa_power_csv(path):
    """
    Read NASA POWER regional CSV.

    The file contains metadata before the real table,
    so this function finds the row beginning with PARAMETER.
    """
    with path.open(encoding="utf-8-sig", newline="") as file:
        lines = file.readlines()

    header_index = None

    for i, line in enumerate(lines):
        if line.startswith("PARAMETER"):
            header_index = i
            break

    if header_index is None:
        raise ValueError("Could not find the NASA POWER table header.")

    reader = csv.DictReader(lines[header_index:])

    return list(reader)


def calculate_summary(rows):
    """
    Group annual radiation values by latitude and longitude.

    Returns one summary row for each grid point.
    """
    grid_values = defaultdict(list)

    for row in rows:
        year = int(row["YEAR"])

        if 2016 <= year <= 2025:
            lat = float(row["LAT"])
            lon = float(row["LON"])
            annual_radiation = float(row["ANN"])

            grid_values[(lat, lon)].append(annual_radiation)

    summary = []

    for (lat, lon), values in grid_values.items():

        mean_radiation = mean(values)
        variability = pstdev(values)

        summary.append(
            {
                "LAT": lat,
                "LON": lon,
                "MEAN_RADIATION": round(mean_radiation, 2),
                "STD_RADIATION": round(variability, 2),
                "YEARS": len(values),
            }
        )

    return summary


def save_summary(rows, path):
    """Save the processed grid data as a new CSV."""
    fieldnames = [
        "LAT",
        "LON",
        "MEAN_RADIATION",
        "STD_RADIATION",
        "YEARS",
    ]

    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(rows)


def main():
    rows = read_nasa_power_csv(INPUT_FILE)

    print(f"NASA data rows: {len(rows)}")

    summary = calculate_summary(rows)

    print(f"Grid points: {len(summary)}")

    save_summary(summary, OUTPUT_FILE)

    print(f"Saved processed data to:")
    print(OUTPUT_FILE)

    print("\nFirst 5 grid points:")

    for row in summary[:5]:
        print(row)


if __name__ == "__main__":
    main()