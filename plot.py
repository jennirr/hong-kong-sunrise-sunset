# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///

import csv
from pathlib import Path
from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


ROOT = Path(__file__).parent
DATA_FILE = ROOT / "data" / "Sun_rise_set_2026.csv"
OUTPUT_FILE = ROOT / "out" / "08-wide-year-of-light.png"


def time_to_hours(time_string):
    """Convert a time such as 07:03 into decimal hours."""
    hour, minute = map(int, time_string.split(":"))
    return hour + minute / 60


def load_data(path):
    dates = []
    sunrise = []
    sunset = []

    with path.open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            dates.append(datetime.strptime(row["YYYY-MM-DD"], "%Y-%m-%d"))
            sunrise.append(time_to_hours(row["RISE"]))
            sunset.append(time_to_hours(row["SET"]))

    return dates, np.array(sunrise), np.array(sunset)


def get_month_positions(dates):
    positions = []
    labels = []

    for i, date in enumerate(dates):
        if date.day == 1:
            positions.append(i)
            labels.append(date.strftime("%b").upper())

    return positions, labels


def main():
    dates, sunrise, sunset = load_data(DATA_FILE)
    daylight = sunset - sunrise
    x = np.arange(len(dates))

    # -----------------------------
    # style
    # -----------------------------
    background = "#F6F2EA"   # warm off-white
    text = "#2E2A26"
    secondary = "#7C746B"
    grid = "#DDD6CB"

    # 柔和暖色，不要太炸
    cmap = LinearSegmentedColormap.from_list(
        "soft_sunlight",
        [
            "#E98A6B",  # soft coral
            "#F1AE62",  # warm orange
            "#F3D685",  # pale yellow
            "#F0B071",  # peach
        ]
    )

    d_min = daylight.min()
    d_max = daylight.max()
    norm = (daylight - d_min) / (d_max - d_min)
    colors = [cmap(v) for v in norm]

    # -----------------------------
    # figure
    # -----------------------------
    fig = plt.figure(figsize=(18, 7), facecolor=background)
    ax = fig.add_axes([0.06, 0.20, 0.91, 0.60], facecolor=background)

    # month guides
    month_positions, month_labels = get_month_positions(dates)
    for pos in month_positions:
        ax.axvline(pos - 0.5, color=grid, linewidth=0.7, alpha=0.45, zorder=0)

    # main visual: one line per day
    ax.vlines(
        x,
        sunrise,
        sunset,
        colors=colors,
        linewidth=1.15,
        alpha=0.95,
        zorder=2
    )

    # -----------------------------
    # axes formatting
    # -----------------------------
    ax.set_xlim(-2, len(dates) + 1)
    ax.set_ylim(19.6, 4.8)

    ax.set_xticks(month_positions)
    ax.set_xticklabels(month_labels, fontsize=11, color=secondary)

    ax.set_yticks([5, 7, 9, 12, 15, 17, 19])
    ax.set_yticklabels(
        ["05:00", "07:00", "09:00", "12:00", "15:00", "17:00", "19:00"],
        fontsize=10,
        color=secondary
    )

    ax.grid(axis="y", color=grid, linewidth=0.7, alpha=0.18)

    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.tick_params(axis="both", length=0, pad=8)

    # -----------------------------
    # title / minimal text
    # -----------------------------
    fig.text(
        0.06, 0.90,
        "HONG KONG SUNRISE / SUNSET",
        fontsize=26,
        fontweight="bold",
        color=text
    )

    fig.text(
        0.06, 0.855,
        "365 days of daylight across 2026",
        fontsize=12,
        color=secondary
    )

    fig.text(
        0.97, 0.90,
        "2026",
        ha="right",
        fontsize=20,
        fontweight="bold",
        color="#D98E6C"
    )

    fig.text(
        0.97, 0.08,
        "Source: Hong Kong Observatory",
        ha="right",
        fontsize=8,
        color=secondary
    )

    # -----------------------------
    # save
    # -----------------------------
    OUTPUT_FILE.parent.mkdir(exist_ok=True)

    plt.savefig(
        OUTPUT_FILE,
        dpi=250,
        facecolor=fig.get_facecolor(),
        bbox_inches="tight"
    )
    plt.show()


if __name__ == "__main__":
    main()