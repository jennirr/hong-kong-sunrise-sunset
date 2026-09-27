# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///

import csv
from pathlib import Path
from datetime import datetime

import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.dates as mdates


ROOT = Path(__file__).parent
DATA_FILE = ROOT / "data" / "Sun_rise_set_2026.csv"
OUTPUT_FILE = ROOT / "out" / "04-light-barcode-poster.png"


def time_to_hours(time_string: str) -> float:
    """Convert HH:MM to decimal hours."""
    hour, minute = map(int, time_string.split(":"))
    return hour + minute / 60


def hours_to_label(hours_float: float) -> str:
    """Convert decimal hours to 'Hh Mm'."""
    h = int(hours_float)
    m = int(round((hours_float - h) * 60))
    if m == 60:
        h += 1
        m = 0
    return f"{h} h {m:02d} m"


def load_data():
    dates = []
    sunrise = []
    sunset = []
    daylight = []

    with open(DATA_FILE, encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        for row in reader:
            d = datetime.strptime(row["YYYY-MM-DD"], "%Y-%m-%d")
            rise = time_to_hours(row["RISE"])
            sett = time_to_hours(row["SET"])
            light = sett - rise

            dates.append(d)
            sunrise.append(rise)
            sunset.append(sett)
            daylight.append(light)

    return dates, sunrise, sunset, daylight


def build_segments(dates, sunrise, sunset):
    """Build vertical line segments for LineCollection."""
    x = mdates.date2num(dates)
    segments = []

    for xi, y1, y2 in zip(x, sunrise, sunset):
        segments.append([(xi, y1), (xi, y2)])

    return segments


def find_stats(dates, sunrise, sunset, daylight):
    longest_i = daylight.index(max(daylight))
    shortest_i = daylight.index(min(daylight))
    earliest_i = sunrise.index(min(sunrise))
    latest_i = sunset.index(max(sunset))

    return {
        "longest_day": (dates[longest_i], daylight[longest_i]),
        "shortest_day": (dates[shortest_i], daylight[shortest_i]),
        "earliest_sunrise": (dates[earliest_i], sunrise[earliest_i]),
        "latest_sunset": (dates[latest_i], sunset[latest_i]),
    }


def main():
    dates, sunrise, sunset, daylight = load_data()
    stats = find_stats(dates, sunrise, sunset, daylight)

    # ---- style ----
    bg = "#f5f1e8"
    text_main = "#1f1f1f"
    text_sub = "#66625c"
    grid = "#d8d2c8"

    # warm light palette
    cmap = LinearSegmentedColormap.from_list(
        "sunlight",
        ["#d94b3d", "#f08a4b", "#f5c35b", "#f8df7a", "#f08a4b", "#d94b3d"]
    )

    # normalize color by daylight length
    d_min = min(daylight)
    d_max = max(daylight)
    norm = [(d - d_min) / (d_max - d_min) if d_max > d_min else 0.5 for d in daylight]
    colors = [cmap(v) for v in norm]

    # ---- figure ----
    fig = plt.figure(figsize=(8, 11), facecolor=bg)

    # main barcode chart
    ax = fig.add_axes([0.08, 0.23, 0.84, 0.56], facecolor=bg)

    segments = build_segments(dates, sunrise, sunset)
    lc = LineCollection(segments, colors=colors, linewidths=1.2, alpha=0.95)
    ax.add_collection(lc)

    # axes limits
    ax.set_xlim(mdates.date2num(dates[0]), mdates.date2num(dates[-1]))
    ax.set_ylim(19.5, 5.0)  # inverted so early time is at top

    # month labels
    month_starts = [datetime(2026, m, 1) for m in range(1, 13)]
    month_labels = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN",
                    "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]

    ax.set_xticks([mdates.date2num(d) for d in month_starts])
    ax.set_xticklabels(month_labels, fontsize=9, color=text_sub)

    # time labels
    ax.set_yticks([5, 8, 11, 14, 17, 19.5])
    ax.set_yticklabels(["05:00", "08:00", "11:00", "14:00", "17:00", "19:30"],
                       fontsize=9, color=text_sub)

    # grid
    ax.grid(axis="x", color=grid, linewidth=0.8, linestyle=":", alpha=0.8)
    ax.grid(axis="y", color=grid, linewidth=0.6, linestyle=":", alpha=0.3)

    # remove spines/ticks
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(axis="both", length=0)

    # ---- title ----
    fig.text(0.08, 0.93, "HONG KONG", fontsize=26, weight="bold", color=text_main)
    fig.text(0.08, 0.905, "SUNRISE / SUNSET", fontsize=26, weight="bold", color=text_main)
    fig.text(0.08, 0.865, "365 DAYS OF LIGHT · 2026", fontsize=14, color=text_main)

    fig.text(
        0.92, 0.93,
        "SAME CITY\nDIFFERENT SKIES\n365 SUNRISES\n365 SUNSETS",
        fontsize=8, color=text_sub, ha="right", va="top", linespacing=1.8
    )

    # ---- short description ----
    fig.text(
        0.08, 0.84,
        "Each vertical stroke marks one day.\n"
        "Top edge = sunrise, bottom edge = sunset, height = daylight duration.",
        fontsize=9, color=text_sub, linespacing=1.5
    )

    # ---- stats row ----
    x_positions = [0.10, 0.33, 0.56, 0.79]
    labels = ["LONGEST DAY", "SHORTEST DAY", "EARLIEST SUNRISE", "LATEST SUNSET"]

    values = [
        (
            stats["longest_day"][0].strftime("%d %b").upper(),
            hours_to_label(stats["longest_day"][1]),
        ),
        (
            stats["shortest_day"][0].strftime("%d %b").upper(),
            hours_to_label(stats["shortest_day"][1]),
        ),
        (
            stats["earliest_sunrise"][0].strftime("%d %b").upper(),
            f"{int(stats['earliest_sunrise'][1]):02d}:{int(round((stats['earliest_sunrise'][1] % 1) * 60)):02d}",
        ),
        (
            stats["latest_sunset"][0].strftime("%d %b").upper(),
            f"{int(stats['latest_sunset'][1]):02d}:{int(round((stats['latest_sunset'][1] % 1) * 60)):02d}",
        ),
    ]

    for x, label, (date_text, value_text) in zip(x_positions, labels, values):
        fig.text(x, 0.155, label, fontsize=8, color=text_sub, weight="bold")
        fig.text(x, 0.128, date_text, fontsize=16, color=text_main, weight="bold")
        fig.text(x, 0.098, value_text, fontsize=12, color=text_main)

    # ---- small daylight curve at bottom ----
    ax2 = fig.add_axes([0.08, 0.05, 0.84, 0.07], facecolor=bg)
    ax2.plot(dates, daylight, color="#e67c52", linewidth=1.5)
    ax2.fill_between(dates, daylight, [min(daylight)] * len(daylight),
                     color="#f1c27d", alpha=0.28)

    ax2.set_xlim(dates[0], dates[-1])
    ax2.set_ylim(min(daylight) - 0.2, max(daylight) + 0.2)

    for spine in ["top", "right", "left"]:
        ax2.spines[spine].set_visible(False)
    ax2.spines["bottom"].set_color(grid)

    ax2.tick_params(axis="y", left=False, labelleft=False)
    ax2.tick_params(axis="x", colors=text_sub, labelsize=7)
    ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))

    ax2.set_title("DAYLIGHT LENGTH THROUGH THE YEAR", loc="left",
                  fontsize=8, color=text_sub, pad=6, weight="bold")

    # ---- source ----
    fig.text(0.92, 0.03, "Source: Hong Kong Observatory",
             fontsize=7, color=text_sub, ha="right")

    OUTPUT_FILE.parent.mkdir(exist_ok=True)
    plt.savefig(OUTPUT_FILE, dpi=300, facecolor=bg, bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    main()