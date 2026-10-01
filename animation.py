# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "pillow"]
# ///

import csv
from pathlib import Path
from datetime import datetime

import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.animation import FuncAnimation, PillowWriter


ROOT = Path(__file__).parent
DATA_FILE = ROOT / "data" / "Sun_rise_set_2026.csv"
OUTPUT_FILE = ROOT / "out" / "06-year-of-light-animation.gif"

# ---------- style ----------
BG = "#f5f1e8"
GRID = "#d9d2c7"
TEXT = "#2e2a26"
TEXT_LIGHT = "#7f776d"
ACCENT = "#d48c69"

TITLE = "HONG KONG SUNRISE / SUNSET"
SUBTITLE = "365 days of daylight across 2026"
YEAR_LABEL = "2026"
SOURCE = "Source: Hong Kong Observatory"

FIG_W = 16
FIG_H = 6
FPS = 20
INTERVAL = 40  # ms per frame
SEGMENTS_PER_DAY = 60


def time_to_hours(time_string: str) -> float:
    hour, minute = map(int, time_string.split(":"))
    return hour + minute / 60


def hours_to_hm(hours: float) -> str:
    h = int(hours)
    m = int(round((hours - h) * 60))
    if m == 60:
        h += 1
        m = 0
    return f"{h:02d}:{m:02d}"


def daylight_text(hours: float) -> str:
    h = int(hours)
    m = int(round((hours - h) * 60))
    if m == 60:
        h += 1
        m = 0
    return f"{h}h {m:02d}m"


def lerp_color(c1, c2, t):
    return tuple(c1[i] + (c2[i] - c1[i]) * t for i in range(3))


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) / 255 for i in (0, 2, 4))


def rgb_to_rgba(rgb, a=1.0):
    return (rgb[0], rgb[1], rgb[2], a)


# soft sky palette: dawn -> morning -> noon -> afternoon -> dusk
DAWN = hex_to_rgb("#efb1a2")       # soft pink
MORNING = hex_to_rgb("#f6d58b")    # pale warm yellow
NOON = hex_to_rgb("#fbf7ef")       # almost white
AFTERNOON = hex_to_rgb("#f8ddb0")  # warm cream
DUSK = hex_to_rgb("#efb1a2")       # pink again


def sky_color(progress: float):
    """
    progress: 0..1 within one day's daylight
    """
    if progress < 0.25:
        t = progress / 0.25
        rgb = lerp_color(DAWN, MORNING, t)
    elif progress < 0.5:
        t = (progress - 0.25) / 0.25
        rgb = lerp_color(MORNING, NOON, t)
    elif progress < 0.75:
        t = (progress - 0.5) / 0.25
        rgb = lerp_color(NOON, AFTERNOON, t)
    else:
        t = (progress - 0.75) / 0.25
        rgb = lerp_color(AFTERNOON, DUSK, t)
    return rgb


def load_data():
    dates = []
    sunrise = []
    sunset = []

    with DATA_FILE.open(encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        for row in reader:
            dates.append(datetime.strptime(row["YYYY-MM-DD"], "%Y-%m-%d"))
            sunrise.append(time_to_hours(row["RISE"]))
            sunset.append(time_to_hours(row["SET"]))

    return dates, sunrise, sunset


def build_day_segments(x, y1, y2, alpha=0.45, width=1.1):
    """
    Make one vertical daylight bar using many short colored segments.
    """
    segments = []
    colors = []
    ys = [y1 + (y2 - y1) * i / SEGMENTS_PER_DAY for i in range(SEGMENTS_PER_DAY + 1)]

    for i in range(SEGMENTS_PER_DAY):
        y_start = ys[i]
        y_end = ys[i + 1]
        p = i / (SEGMENTS_PER_DAY - 1)
        color = rgb_to_rgba(sky_color(p), alpha)

        segments.append([(x, y_start), (x, y_end)])
        colors.append(color)

    return LineCollection(
        segments,
        colors=colors,
        linewidths=width,
        capstyle="butt",
        zorder=3
    )


def build_background(ax, dates, sunrise, sunset):
    for i, (sr, ss) in enumerate(zip(sunrise, sunset)):
        lc = build_day_segments(i, sr, ss, alpha=0.45, width=1.1)
        ax.add_collection(lc)


def add_labels(fig, ax, dates, sunrise, sunset):
    # Title block
    fig.text(0.055, 0.92, TITLE, fontsize=30, fontweight="bold", color=TEXT)
    fig.text(0.055, 0.875, SUBTITLE, fontsize=15, color=TEXT_LIGHT)
    fig.text(0.93, 0.91, YEAR_LABEL, ha="right", fontsize=24, fontweight="bold", color=ACCENT)

    # Source
    fig.text(0.93, 0.06, SOURCE, ha="right", fontsize=10, color=TEXT_LIGHT)

    # Month ticks
    month_positions = []
    month_labels = []
    current_month = None
    for i, d in enumerate(dates):
        if d.month != current_month:
            month_positions.append(i)
            month_labels.append(d.strftime("%b").upper())
            current_month = d.month

    ax.set_xticks(month_positions)
    ax.set_xticklabels(month_labels, fontsize=12, color=TEXT_LIGHT)

    # Y ticks
    yticks = [5, 7, 9, 12, 15, 17, 19]
    ax.set_yticks(yticks)
    ax.set_yticklabels([f"{int(y):02d}:00" for y in yticks], fontsize=12, color=TEXT_LIGHT)

    # grid
    ax.grid(axis="x", color=GRID, linewidth=0.8, alpha=0.6)
    ax.grid(axis="y", color=GRID, linewidth=0.8, alpha=0.35)

    # limits and style
    ax.set_xlim(-5, len(dates) + 5)
    ax.set_ylim(19.5, 4.5)  # invert so early morning is at top

    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.tick_params(length=0)
    ax.set_facecolor(BG)


def main():
    dates, sunrise, sunset = load_data()
    daylight = [ss - sr for sr, ss in zip(sunrise, sunset)]

    OUTPUT_FILE.parent.mkdir(exist_ok=True)

    fig = plt.figure(figsize=(FIG_W, FIG_H), facecolor=BG)
    ax = fig.add_axes([0.05, 0.18, 0.92, 0.64])
    ax.set_facecolor(BG)

    # background: all days
    build_background(ax, dates, sunrise, sunset)
    add_labels(fig, ax, dates, sunrise, sunset)

    # animated highlight
    highlight = build_day_segments(0, sunrise[0], sunset[0], alpha=0.95, width=3.0)
    ax.add_collection(highlight)

    # current-day text
    info_text = fig.text(
        0.055, 0.085,
        "",
        fontsize=12,
        color=TEXT_LIGHT
    )

    # optional subtle guide line at current day
    current_line = ax.axvline(0, color="#c8b8a7", linewidth=0.8, alpha=0.35, zorder=1)

    def update(frame):
        d = dates[frame]
        sr = sunrise[frame]
        ss = sunset[frame]
        dl = daylight[frame]

        new_highlight = build_day_segments(frame, sr, ss, alpha=0.95, width=3.0)
        highlight.set_segments(new_highlight.get_segments())
        highlight.set_colors(new_highlight.get_colors())
        highlight.set_linewidths(new_highlight.get_linewidths())

        current_line.set_xdata([frame, frame])

        info_text.set_text(
            f"{d.strftime('%d %b %Y')}  ·  "
            f"Sunrise {hours_to_hm(sr)}  ·  "
            f"Sunset {hours_to_hm(ss)}  ·  "
            f"Daylight {daylight_text(dl)}"
        )

        return highlight, info_text, current_line

    anim = FuncAnimation(
        fig,
        update,
        frames=len(dates),
        interval=INTERVAL,
        blit=False,
        repeat=True
    )

    anim.save(OUTPUT_FILE, writer=PillowWriter(fps=FPS))
    print(f"Saved animation to: {OUTPUT_FILE}")

    plt.show()


if __name__ == "__main__":
    main()