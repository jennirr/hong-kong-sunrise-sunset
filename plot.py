# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///

import csv
from pathlib import Path
from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


ROOT = Path(__file__).parent
DATA_FILE = ROOT / "data" / "Sun_rise_set_2026.csv"
OUTPUT_FILE = ROOT / "out" / "06-soft-year-of-light.png"


def time_to_hours(time_string):
    """Convert HH:MM to decimal hours."""
    hour, minute = map(int, time_string.split(":"))
    return hour + minute / 60


def hex_to_rgb(hex_color):
    """#RRGGBB -> (r, g, b) in 0-1 range."""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) / 255 for i in (0, 2, 4))


def build_soft_warm_colormap():
    """
    A low-saturation warm palette:
    dusty coral -> apricot -> pale gold -> warm cream -> muted peach -> coral
    """
    palette = [
        "#E8A09A",  # dusty coral pink
        "#EDB28D",  # soft apricot
        "#F1D6A2",  # pale gold
        "#F5E6C8",  # warm cream
        "#EFC3A3",  # muted peach
        "#E5A098",  # soft coral
    ]
    rgb_palette = [hex_to_rgb(c) for c in palette]
    return LinearSegmentedColormap.from_list("soft_warm_light", rgb_palette, N=365)


def read_data():
    dates = []
    sunrise = []
    sunset = []

    with open(DATA_FILE, encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        for row in reader:
            dates.append(datetime.strptime(row["YYYY-MM-DD"], "%Y-%m-%d"))
            sunrise.append(time_to_hours(row["RISE"]))
            sunset.append(time_to_hours(row["SET"]))

    return dates, sunrise, sunset


def month_positions(dates):
    positions = []
    labels = []
    seen = set()

    for i, d in enumerate(dates):
        key = (d.year, d.month)
        if key not in seen:
            seen.add(key)
            positions.append(i)
            labels.append(d.strftime("%b").upper())

    return positions, labels


def main():
    dates, sunrise, sunset = read_data()

    x = np.arange(len(dates))
    sunrise = np.array(sunrise)
    sunset = np.array(sunset)
    daylight = sunset - sunrise

    # key stats
    longest_idx = int(np.argmax(daylight))
    shortest_idx = int(np.argmin(daylight))
    earliest_sunrise_idx = int(np.argmin(sunrise))
    latest_sunset_idx = int(np.argmax(sunset))

    # color mapping across the year
    cmap = build_soft_warm_colormap()
    colors = [cmap(i / (len(x) - 1)) for i in x]

    # figure / axes
    fig = plt.figure(figsize=(16, 9), dpi=200, facecolor="#F4F0E8")
    ax = fig.add_axes([0.055, 0.24, 0.91, 0.56])  # left, bottom, width, height
    ax.set_facecolor("#F4F0E8")

    # draw one vertical line per day
    for i in range(len(x)):
        ax.plot(
            [x[i], x[i]],
            [sunrise[i], sunset[i]],
            color=colors[i],
            linewidth=1.35,
            alpha=0.95,
            solid_capstyle="butt",
        )

    # axes styling
    ax.set_xlim(-5, len(x) + 5)
    ax.set_ylim(19.6, 4.8)  # inverted so earlier times appear higher

    month_x, month_labels = month_positions(dates)
    ax.set_xticks(month_x)
    ax.set_xticklabels(month_labels, fontsize=12, color="#7D7468")

    y_ticks = [5, 7, 9, 12, 15, 17, 19]
    ax.set_yticks(y_ticks)
    ax.set_yticklabels([f"{int(t):02d}:00" for t in y_ticks], fontsize=11, color="#7D7468")

    # subtle grid
    ax.grid(axis="x", color="#DED8CC", linewidth=0.8, alpha=0.6)
    ax.grid(axis="y", color="#E8E1D5", linewidth=0.6, alpha=0.35)

    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.tick_params(axis="both", length=0, pad=8)

    # title block
    fig.text(
        0.055, 0.895,
        "A YEAR OF LIGHT",
        fontsize=30,
        fontweight="bold",
        color="#2A2623",
        ha="left", va="top"
    )
    fig.text(
        0.055, 0.855,
        "Hong Kong sunrise and sunset across 2026",
        fontsize=14,
        color="#7D7468",
        ha="left", va="top"
    )
    fig.text(
        0.055, 0.828,
        "One vertical line = one day",
        fontsize=11,
        color="#A09487",
        ha="left", va="top"
    )

    # small annotations (minimal version)
    fig.text(
        0.055, 0.15,
        f"Longest day  {dates[longest_idx].strftime('%d %b')}  ·  {int(daylight[longest_idx])}h {round((daylight[longest_idx] % 1) * 60):02d}m",
        fontsize=12,
        color="#4D4741",
        ha="left",
    )

    fig.text(
        0.34, 0.15,
        f"Shortest day  {dates[shortest_idx].strftime('%d %b')}  ·  {int(daylight[shortest_idx])}h {round((daylight[shortest_idx] % 1) * 60):02d}m",
        fontsize=12,
        color="#4D4741",
        ha="left",
    )

    fig.text(
        0.64, 0.15,
        f"Earliest sunrise  {dates[earliest_sunrise_idx].strftime('%d %b')}  ·  {int(sunrise[earliest_sunrise_idx]):02d}:{round((sunrise[earliest_sunrise_idx] % 1) * 60):02d}",
        fontsize=12,
        color="#4D4741",
        ha="left",
    )

    fig.text(
        0.64, 0.115,
        f"Latest sunset  {dates[latest_sunset_idx].strftime('%d %b')}  ·  {int(sunset[latest_sunset_idx]):02d}:{round((sunset[latest_sunset_idx] % 1) * 60):02d}",
        fontsize=12,
        color="#4D4741",
        ha="left",
    )

    # source
    fig.text(
        0.965, 0.055,
        "Source: Hong Kong Observatory",
        fontsize=10,
        color="#9B9084",
        ha="right",
    )

    # save
    OUTPUT_FILE.parent.mkdir(exist_ok=True)
    plt.savefig(OUTPUT_FILE, dpi=200, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    main()