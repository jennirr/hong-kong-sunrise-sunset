# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///

import csv
import math
from pathlib import Path
from datetime import datetime

import matplotlib.pyplot as plt

ROOT = Path(__file__).parent
DATA_FILE = ROOT / "data" / "Sun_rise_set_2026.csv"
OUTPUT_FILE = ROOT / "out" / "first-plot.png"


def time_to_hours(time_string):
    """Convert a time such as 07:03 into decimal hours."""
    hour, minute = map(int, time_string.split(":"))
    return hour + minute / 60


dates = []
sunrise = []
sunset = []

with open(DATA_FILE, encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)
    for row in reader:
        dates.append(datetime.strptime(row["YYYY-MM-DD"], "%Y-%m-%d"))
        sunrise.append(time_to_hours(row["RISE"]))
        sunset.append(time_to_hours(row["SET"]))

count = len(dates)

# One angle per day
theta = [2 * math.pi * i / count for i in range(count)]

# Close the circle
theta.append(theta[0])
sunrise.append(sunrise[0])
sunset.append(sunset[0])

fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={"projection": "polar"})

# Background
fig.patch.set_facecolor("#f8f3e8")
ax.set_facecolor("#f8f3e8")

# Put January at the top, move clockwise
ax.set_theta_zero_location("N")
ax.set_theta_direction(-1)

# Draw daylight area
ax.fill_between(
    theta,
    sunrise,
    sunset,
    color="#f6c453",
    alpha=0.45,
    linewidth=0
)

# Draw sunrise and sunset lines
ax.plot(theta, sunrise, color="#e07a2d", linewidth=2.2, label="Sunrise")
ax.plot(theta, sunset, color="#d1495b", linewidth=2.2, label="Sunset")

# Radial range: focus on the useful part of the day
ax.set_ylim(4, 20)

# Cleaner grid
ax.grid(color="#999999", alpha=0.25, linewidth=0.8)
ax.spines["polar"].set_visible(False)

# Radial labels = time
ax.set_yticks([6, 9, 12, 15, 18])
ax.set_yticklabels(["6:00", "9:00", "12:00", "15:00", "18:00"], fontsize=10, color="#555555")

# Month labels
month_starts = [
    datetime(2026, 1, 1), datetime(2026, 2, 1), datetime(2026, 3, 1),
    datetime(2026, 4, 1), datetime(2026, 5, 1), datetime(2026, 6, 1),
    datetime(2026, 7, 1), datetime(2026, 8, 1), datetime(2026, 9, 1),
    datetime(2026, 10, 1), datetime(2026, 11, 1), datetime(2026, 12, 1)
]
month_angles = [2 * math.pi * (d.timetuple().tm_yday - 1) / count for d in month_starts]
month_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
ax.set_xticks(month_angles)
ax.set_xticklabels(month_labels, fontsize=11, color="#444444")

# Title
ax.set_title(
    "Hong Kong Sunrise and Sunset, 2026",
    va="bottom",
    fontsize=18,
    color="#222222",
    pad=30
)

# Optional small subtitle in the centre
ax.text(
    0.5, 0.5,
    "Daylight\nthrough a year",
    transform=ax.transAxes,
    ha="center",
    va="center",
    fontsize=16,
    color="#444444"
)

OUTPUT_FILE.parent.mkdir(exist_ok=True)
plt.tight_layout()
plt.savefig(OUTPUT_FILE, dpi=200, facecolor=fig.get_facecolor())
plt.show()