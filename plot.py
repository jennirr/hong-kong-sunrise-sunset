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
OUTPUT_FILE = ROOT / "out" / "07-final-year-of-light.png"


def time_to_hours(time_string):
    """Convert '07:03' into decimal hours."""
    hour, minute = map(int, time_string.split(":"))
    return hour + minute / 60


def load_data(path):
    """Read sunrise and sunset data from the HKO CSV."""
    dates = []
    sunrise = []
    sunset = []

    with path.open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            dates.append(
                datetime.strptime(row["YYYY-MM-DD"], "%Y-%m-%d")
            )
            sunrise.append(time_to_hours(row["RISE"]))
            sunset.append(time_to_hours(row["SET"]))

    return dates, sunrise, sunset


def build_sky_colormap():
    """
    Artistic sky palette from sunrise to sunset.

    These colours are not measured sky-colour data.
    They are used as an artistic mapping to suggest
    changing daylight through one day.
    """
    colors = [
        "#E9B1A5",  # soft sunrise rose
        "#F0C4A4",  # pale peach
        "#F3D9AE",  # warm morning light
        "#EAE8DA",  # hazy daylight
        "#D9E2E5",  # pale sky blue-grey
        "#E8E1C9",  # soft afternoon light
        "#EDC8AC",  # muted peach
        "#DFA9A8",  # dusty sunset rose
    ]

    return LinearSegmentedColormap.from_list(
        "soft_sky",
        colors
    )


def draw_gradient_day(
    ax,
    x,
    sunrise,
    sunset,
    cmap,
    segments=70,
    linewidth=1.1,
    alpha=0.90,
):
    """Draw one day as a vertical sunrise-to-sunset colour gradient."""

    y_values = [
        sunrise + (sunset - sunrise) * i / segments
        for i in range(segments + 1)
    ]

    line_segments = []
    line_colors = []

    for i in range(segments):
        line_segments.append(
            [
                (x, y_values[i]),
                (x, y_values[i + 1])
            ]
        )

        progress = i / max(1, segments - 1)

        line_colors.append(
            to_rgba(
                cmap(progress),
                alpha=alpha
            )
        )

    collection = LineCollection(
        line_segments,
        colors=line_colors,
        linewidths=linewidth,
        capstyle="butt"
    )

    ax.add_collection(collection)


def main():
    dates, sunrise, sunset = load_data(DATA_FILE)

    background = "#F5F1E8"
    text = "#2D2926"
    secondary = "#817A72"
    grid = "#DCD5C9"

    cmap = build_sky_colormap()

    # Wider horizontal format
    fig = plt.figure(
        figsize=(20, 6.5),
        dpi=200,
        facecolor=background
    )

    ax = fig.add_axes(
        [0.045, 0.18, 0.925, 0.64],
        facecolor=background
    )

    # Draw one line for every day
    for i in range(len(dates)):
        draw_gradient_day(
            ax,
            i,
            sunrise[i],
            sunset[i],
            cmap,
            segments=70,
            linewidth=1.1,
            alpha=0.90,
        )

    # -----------------------------
    # Axes
    # -----------------------------

    ax.set_xlim(-3, len(dates) + 2)
    ax.set_ylim(19.5, 4.5)

    y_ticks = [5, 7, 9, 12, 15, 17, 19]

    ax.set_yticks(y_ticks)

    ax.set_yticklabels(
        [f"{int(t):02d}:00" for t in y_ticks],
        fontsize=10,
        color=secondary
    )

    ax.tick_params(
        axis="y",
        length=0,
        pad=9
    )

    ax.set_xticks([])

    # Subtle horizontal guides
    for y in y_ticks:
        ax.axhline(
            y,
            color=grid,
            linewidth=0.7,
            alpha=0.28,
            zorder=0
        )

    # -----------------------------
    # Month labels
    # -----------------------------

    month_starts = []
    month_labels = []

    last_month = None

    for i, date in enumerate(dates):
        if date.month != last_month:
            month_starts.append(i)
            month_labels.append(date.strftime("%b").upper())
            last_month = date.month

    for position in month_starts:
        ax.axvline(
            position - 0.5,
            color=grid,
            linewidth=0.7,
            alpha=0.28,
            zorder=0
        )

    for position, label in zip(month_starts, month_labels):
        ax.text(
            position,
            19.82,
            label,
            ha="left",
            va="top",
            fontsize=10,
            color=secondary
        )

    # Remove frame
    for spine in ax.spines.values():
        spine.set_visible(False)

    # -----------------------------
    # Title
    # -----------------------------

    fig.text(
        0.045,
        0.91,
        "A YEAR OF LIGHT",
        fontsize=30,
        fontweight="bold",
        color=text,
        ha="left"
    )

    fig.text(
        0.045,
        0.86,
        "Hong Kong sunrise and sunset · 2026",
        fontsize=13,
        color=secondary,
        ha="left"
    )

    # -----------------------------
    # Source
    # -----------------------------

    fig.text(
        0.97,
        0.065,
        "Source · Hong Kong Observatory",
        fontsize=9,
        color=secondary,
        ha="right"
    )

    # -----------------------------
    # Save
    # -----------------------------

    OUTPUT_FILE.parent.mkdir(exist_ok=True)

    plt.savefig(
        OUTPUT_FILE,
        dpi=220,
        facecolor=fig.get_facecolor(),
        bbox_inches="tight"
    )

    plt.show()


if __name__ == "__main__":
    main()