# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///

import csv
from pathlib import Path
from datetime import datetime

import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap, to_rgba


ROOT = Path(__file__).parent
DATA_FILE = ROOT / "data" / "Sun_rise_set_2026.csv"
OUTPUT_FILE = ROOT / "out" / "06-sky-gradient-year.png"


def time_to_hours(time_string):
    """Convert '07:03' to decimal hours."""
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

    return dates, sunrise, sunset


def build_sky_cmap():
    """
    A soft sky palette for one day:
    sunrise pink -> warm peach -> soft gold -> pale sky -> warm light -> sunset rose
    """
    colors = [
        "#E8AEA3",  # soft rose
        "#F0C29F",  # peach
        "#F5D9A6",  # pale gold
        "#E8E6D8",  # hazy daylight
        "#D8E1E4",  # pale sky blue-grey
        "#EEE0BE",  # warm afternoon light
        "#EDC2A7",  # peach again
        "#DCA4A6",  # dusty sunset rose
    ]
    return LinearSegmentedColormap.from_list("soft_sky", colors)


def make_gradient_line(ax, x, y0, y1, cmap, n_segments=60, lw=1.2, alpha=0.95):
    """
    Draw one vertical line from y0 to y1 using many short segments,
    so the line itself can have a vertical gradient.
    """
    ys = [y0 + (y1 - y0) * i / n_segments for i in range(n_segments + 1)]

    segments = []
    colors = []

    for i in range(n_segments):
        segments.append([(x, ys[i]), (x, ys[i + 1])])
        t = i / max(1, n_segments - 1)
        colors.append(to_rgba(cmap(t), alpha=alpha))

    lc = LineCollection(segments, colors=colors, linewidths=lw, capstyle="butt")
    ax.add_collection(lc)


def main():
    dates, sunrise, sunset = load_data(DATA_FILE)
    daylight = [set_time - rise_time for rise_time, set_time in zip(sunrise, sunset)]

    x_values = list(range(len(dates)))
    cmap = build_sky_cmap()

    # ---- figure style ----
    bg = "#F5F1E8"        # warm paper
    grid = "#D9D1C5"      # subtle grid
    text = "#2A2725"      # dark text
    subtext = "#7E776E"   # muted text

    fig = plt.figure(figsize=(20, 6.8), dpi=200, facecolor=bg)
    ax = fig.add_axes([0.05, 0.23, 0.92, 0.58], facecolor=bg)

    # ---- draw 365 gradient lines ----
    for x, y0, y1 in zip(x_values, sunrise, sunset):
        make_gradient_line(ax, x, y0, y1, cmap, n_segments=60, lw=1.15, alpha=0.95)

    # ---- axes ----
    ax.set_xlim(-2, len(dates) + 1)
    ax.set_ylim(19.5, 4.5)  # inverted so morning is near top

    ax.set_xticks([])
    y_ticks = [5, 7, 9, 12, 15, 17, 19]
    ax.set_yticks(y_ticks)
    ax.set_yticklabels([f"{int(t):02d}:00" for t in y_ticks], fontsize=11, color=subtext)

    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.tick_params(axis="y", length=0)

    # horizontal guide lines
    for y in y_ticks:
        ax.axhline(y, color=grid, lw=0.8, alpha=0.35, zorder=0)

    # month separators + month labels
    month_starts = []
    month_labels = []
    last_month = None

    for i, d in enumerate(dates):
        if d.month != last_month:
            month_starts.append(i)
            month_labels.append(d.strftime("%b").upper())
            last_month = d.month

    for x in month_starts:
        ax.axvline(x - 0.5, color=grid, lw=0.8, alpha=0.35, zorder=0)

    for x, label in zip(month_starts, month_labels):
        ax.text(
            x,
            19.9,
            label,
            ha="left",
            va="top",
            fontsize=11,
            color=subtext
        )

    # ---- titles ----
    fig.text(
        0.05, 0.91,
        "HONG KONG SUNRISE / SUNSET",
        fontsize=28,
        fontweight="bold",
        color=text,
        family="sans-serif"
    )

    fig.text(
        0.05, 0.865,
        "365 days of daylight across 2026",
        fontsize=14,
        color=subtext
    )

    fig.text(
        0.965, 0.91,
        "2026",
        ha="right",
        fontsize=24,
        fontweight="bold",
        color="#D58C67"
    )

    # ---- quiet annotation ----
    longest_idx = daylight.index(max(daylight))
    shortest_idx = daylight.index(min(daylight))

    longest_day = daylight[longest_idx]
    shortest_day = daylight[shortest_idx]

    def format_duration(hours):
        total_minutes = round(hours * 60)
        h = total_minutes // 60
        m = total_minutes % 60
        return f"{h}h {m:02d}m"

    fig.text(
        0.05, 0.11,
        f"Longest daylight  {dates[longest_idx].strftime('%d %b')}  ·  {format_duration(longest_day)}",
        fontsize=11,
        color=subtext
    )

    fig.text(
        0.34, 0.11,
        f"Shortest daylight  {dates[shortest_idx].strftime('%d %b')}  ·  {format_duration(shortest_day)}",
        fontsize=11,
        color=subtext
    )

    fig.text(
        0.965, 0.11,
        "Source: Hong Kong Observatory",
        ha="right",
        fontsize=10,
        color=subtext
    )

    # ---- save ----
    OUTPUT_FILE.parent.mkdir(exist_ok=True)
    plt.savefig(OUTPUT_FILE, facecolor=bg, bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    main()