# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "pillow"]
# ///

import csv
from pathlib import Path
from datetime import datetime

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap


# --------------------------------------------------
# PATHS
# --------------------------------------------------

ROOT = Path(__file__).parent
DATA_FILE = ROOT / "data" / "Sun_rise_set_2026.csv"
OUTPUT_FILE = ROOT / "out" / "07-year-of-light-animation.gif"


# --------------------------------------------------
# VISUAL SETTINGS
# --------------------------------------------------

BACKGROUND = "#F5F1E8"
TEXT = "#2D2926"
SECONDARY = "#817A72"
GRID = "#DCD5C9"

# Background lines
BASE_ALPHA = 0.42
BASE_WIDTH = 1.0

# Current day
HIGHLIGHT_ALPHA = 1.0
HIGHLIGHT_WIDTH = 3.0

# Each day is divided into this many colour sections.
# 24 is enough for a smooth-looking gradient but much faster than 60.
SEGMENTS_PER_DAY = 24

FPS = 18


# --------------------------------------------------
# DATA
# --------------------------------------------------

def time_to_hours(time_string):
    """Convert 07:03 to decimal hours."""
    hour, minute = map(int, time_string.split(":"))
    return hour + minute / 60


def format_time(hours):
    """Convert decimal hours back to HH:MM."""
    total_minutes = round(hours * 60)

    hour = total_minutes // 60
    minute = total_minutes % 60

    return f"{hour:02d}:{minute:02d}"


def format_duration(hours):
    """Convert decimal hours into 13h 30m."""
    total_minutes = round(hours * 60)

    hour = total_minutes // 60
    minute = total_minutes % 60

    return f"{hour}h {minute:02d}m"


def load_data(path):
    dates = []
    sunrise = []
    sunset = []

    with path.open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            dates.append(
                datetime.strptime(
                    row["YYYY-MM-DD"],
                    "%Y-%m-%d"
                )
            )

            sunrise.append(
                time_to_hours(row["RISE"])
            )

            sunset.append(
                time_to_hours(row["SET"])
            )

    return dates, sunrise, sunset


# --------------------------------------------------
# SKY COLOURS
# --------------------------------------------------

def build_sky_colormap():
    """
    Artistic sky colours from sunrise to sunset.

    These colours are not measured sky-colour data.
    They visually suggest the changing atmosphere of daylight.
    """

    colors = [
        "#E6AAA5",  # dawn rose
        "#EFC1A5",  # peach
        "#F3D6AD",  # morning gold
        "#EEE7D5",  # warm daylight
        "#D8E2E4",  # soft pale blue
        "#E4E1D1",  # afternoon haze
        "#EEC5AA",  # late afternoon
        "#DDA5A5",  # sunset rose
    ]

    return LinearSegmentedColormap.from_list(
        "sky",
        colors
    )


SKY_CMAP = build_sky_colormap()


# --------------------------------------------------
# BUILD ONE DAY
# --------------------------------------------------

def day_segments(x, sunrise, sunset):
    """
    Return segments and colours for one vertical day.
    """

    segments = []
    colors = []

    for i in range(SEGMENTS_PER_DAY):

        progress_1 = i / SEGMENTS_PER_DAY
        progress_2 = (i + 1) / SEGMENTS_PER_DAY

        y1 = sunrise + (sunset - sunrise) * progress_1
        y2 = sunrise + (sunset - sunrise) * progress_2

        segments.append(
            [
                (x, y1),
                (x, y2)
            ]
        )

        middle = (
            progress_1 + progress_2
        ) / 2

        colors.append(
            SKY_CMAP(middle)
        )

    return segments, colors


# --------------------------------------------------
# BUILD ALL 365 DAYS ONCE
# --------------------------------------------------

def build_year_background(
    dates,
    sunrise,
    sunset
):

    all_segments = []
    all_colors = []

    for i in range(len(dates)):

        segments, colors = day_segments(
            i,
            sunrise[i],
            sunset[i]
        )

        all_segments.extend(segments)
        all_colors.extend(colors)

    return all_segments, all_colors


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():

    dates, sunrise, sunset = load_data(
        DATA_FILE
    )

    daylight = [
        sunset[i] - sunrise[i]
        for i in range(len(dates))
    ]

    # ----------------------------------------------
    # FIGURE
    # ----------------------------------------------

    # Keep the wide composition,
    # but GIF resolution is intentionally lighter.
    fig = plt.figure(
        figsize=(16, 5.2),
        dpi=100,
        facecolor=BACKGROUND
    )

    ax = fig.add_axes(
        [0.045, 0.20, 0.925, 0.62],
        facecolor=BACKGROUND
    )

    # ----------------------------------------------
    # STATIC YEAR
    # ----------------------------------------------

    background_segments, background_colors = (
        build_year_background(
            dates,
            sunrise,
            sunset
        )
    )

    background_collection = LineCollection(
        background_segments,
        colors=background_colors,
        linewidths=BASE_WIDTH,
        alpha=BASE_ALPHA,
        capstyle="butt",
        zorder=2
    )

    ax.add_collection(
        background_collection
    )

    # ----------------------------------------------
    # CURRENT-DAY HIGHLIGHT
    # ----------------------------------------------

    initial_segments, initial_colors = day_segments(
        0,
        sunrise[0],
        sunset[0]
    )

    highlight = LineCollection(
        initial_segments,
        colors=initial_colors,
        linewidths=HIGHLIGHT_WIDTH,
        alpha=HIGHLIGHT_ALPHA,
        capstyle="butt",
        zorder=5
    )

    ax.add_collection(highlight)

    # A very subtle vertical guide
    guide = ax.axvline(
        0,
        color="#B8AEA3",
        linewidth=0.7,
        alpha=0.35,
        zorder=1
    )

    # ----------------------------------------------
    # AXES
    # ----------------------------------------------

    ax.set_xlim(
        -3,
        len(dates) + 2
    )

    ax.set_ylim(
        19.5,
        4.5
    )

    y_ticks = [
        5,
        7,
        9,
        12,
        15,
        17,
        19
    ]

    ax.set_yticks(y_ticks)

    ax.set_yticklabels(
        [
            f"{int(t):02d}:00"
            for t in y_ticks
        ],
        fontsize=9,
        color=SECONDARY
    )

    ax.tick_params(
        axis="y",
        length=0,
        pad=8
    )

    # ----------------------------------------------
    # MONTHS
    # ----------------------------------------------

    month_positions = []
    month_labels = []

    last_month = None

    for i, date in enumerate(dates):

        if date.month != last_month:

            month_positions.append(i)
            month_labels.append(
                date.strftime("%b").upper()
            )

            last_month = date.month

    ax.set_xticks(
        month_positions
    )

    ax.set_xticklabels(
        month_labels,
        fontsize=9,
        color=SECONDARY
    )

    ax.tick_params(
        axis="x",
        length=0,
        pad=8
    )

    # ----------------------------------------------
    # GRID
    # ----------------------------------------------

    for y in y_ticks:

        ax.axhline(
            y,
            color=GRID,
            linewidth=0.6,
            alpha=0.25,
            zorder=0
        )

    for x in month_positions:

        ax.axvline(
            x - 0.5,
            color=GRID,
            linewidth=0.6,
            alpha=0.25,
            zorder=0
        )

    for spine in ax.spines.values():
        spine.set_visible(False)

    # ----------------------------------------------
    # TITLE — SAME AS STATIC VERSION
    # ----------------------------------------------

    fig.text(
        0.045,
        0.91,
        "A YEAR OF LIGHT",
        fontsize=24,
        fontweight="bold",
        color=TEXT,
        ha="left"
    )

    fig.text(
        0.045,
        0.86,
        "Hong Kong sunrise and sunset · 2026",
        fontsize=11,
        color=SECONDARY,
        ha="left"
    )

    # ----------------------------------------------
    # CURRENT DAY INFORMATION
    # ----------------------------------------------

    info_text = fig.text(
        0.045,
        0.085,
        "",
        fontsize=10,
        color=TEXT,
        ha="left"
    )

    fig.text(
        0.97,
        0.065,
        "Source · Hong Kong Observatory",
        fontsize=8,
        color=SECONDARY,
        ha="right"
    )

    # ----------------------------------------------
    # ANIMATION UPDATE
    # ----------------------------------------------

    def update(frame):

        segments, colors = day_segments(
            frame,
            sunrise[frame],
            sunset[frame]
        )

        highlight.set_segments(
            segments
        )

        highlight.set_color(
            colors
        )

        guide.set_xdata(
            [frame, frame]
        )

        date = dates[frame]

        info_text.set_text(
            f"{date.strftime('%d %b')}   ·   "
            f"Sunrise {format_time(sunrise[frame])}   ·   "
            f"Sunset {format_time(sunset[frame])}   ·   "
            f"Daylight {format_duration(daylight[frame])}"
        )

        return (
            highlight,
            guide,
            info_text
        )

    # ----------------------------------------------
    # CREATE ANIMATION
    # ----------------------------------------------

    animation = FuncAnimation(
        fig,
        update,
        frames=len(dates),
        interval=55,
        blit=True,
        repeat=True
    )

    # ----------------------------------------------
    # SAVE
    # ----------------------------------------------

    OUTPUT_FILE.parent.mkdir(
        exist_ok=True
    )

    print(
        f"Rendering {len(dates)} frames..."
    )

    def show_progress(
        current_frame,
        total_frames
    ):

        # print every ~25 frames
        if (
            current_frame % 25 == 0
            or current_frame + 1 == total_frames
        ):

            print(
                f"Rendering "
                f"{current_frame + 1} / "
                f"{total_frames}"
            )

    animation.save(
        OUTPUT_FILE,
        writer=PillowWriter(
            fps=FPS
        ),
        dpi=90,
        progress_callback=show_progress
    )

    print()
    print(
        "Finished!"
    )

    print(
        f"Saved to: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()