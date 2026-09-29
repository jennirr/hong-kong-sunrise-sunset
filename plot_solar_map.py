# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///

import csv
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).parent
DATA_FILE = ROOT / "data" / "solar_summary_2016_2025.csv"
OUTPUT_FILE = ROOT / "out" / "09-solar-grid-test.png"


def load_summary(path):
    latitudes = []
    longitudes = []
    mean_radiation = []
    variability = []

    with path.open(encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            latitudes.append(float(row["LAT"]))
            longitudes.append(float(row["LON"]))
            mean_radiation.append(float(row["MEAN_RADIATION"]))
            variability.append(float(row["STD_RADIATION"]))

    return latitudes, longitudes, mean_radiation, variability


def scale_sizes(values):
    """
    Convert variability values into visible circle sizes.
    """
    minimum = min(values)
    maximum = max(values)

    sizes = []

    for value in values:
        if maximum == minimum:
            size = 300
        else:
            normalized = (value - minimum) / (maximum - minimum)
            size = 180 + normalized * 900

        sizes.append(size)

    return sizes


def main():
    latitudes, longitudes, mean_radiation, variability = load_summary(DATA_FILE)

    sizes = scale_sizes(variability)

    fig, ax = plt.subplots(figsize=(12, 7))

    scatter = ax.scatter(
        longitudes,
        latitudes,
        c=mean_radiation,
        s=sizes,
        cmap="YlOrRd",
        alpha=0.75,
        edgecolors="white",
        linewidths=1.2
    )

    ax.set_title(
        "Greater Bay Area Solar Radiation — 2016–2025",
        fontsize=18,
        pad=18
    )

    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

    ax.set_xlim(min(longitudes) - 0.5, max(longitudes) + 0.5)
    ax.set_ylim(min(latitudes) - 0.5, max(latitudes) + 0.5)

    ax.grid(
        linestyle="--",
        alpha=0.2
    )

    colorbar = plt.colorbar(scatter, ax=ax)

    colorbar.set_label(
        "Mean solar radiation (W/m²)"
    )

    ax.text(
        0.01,
        0.02,
        "Circle size = interannual variability",
        transform=ax.transAxes,
        fontsize=10
    )

    OUTPUT_FILE.parent.mkdir(exist_ok=True)

    plt.tight_layout()

    plt.savefig(
        OUTPUT_FILE,
        dpi=220,
        bbox_inches="tight"
    )

    plt.show()


if __name__ == "__main__":
    main()