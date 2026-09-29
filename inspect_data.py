import csv
from pathlib import Path

ROOT = Path(__file__).parent
DATA_FILE = ROOT / "data" / "POWER_Regional_Monthly_2016_2025.csv"

with DATA_FILE.open(encoding="utf-8-sig") as file:
    reader = csv.reader(file)

    for i, row in enumerate(reader):
        print(row)

        if i >= 20:
            break