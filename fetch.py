# /// script
# requires-python = ">=3.10"
# dependencies = ["requests"]
# ///

"""
Fetch the Hong Kong Observatory sunrise and sunset data for 2026.

Run:

    uv run fetch.py

The raw CSV file is saved once to data/ and is not fetched again
unless the existing file is deleted.
"""

from pathlib import Path

import requests


URL = (
    "https://data.weather.gov.hk/weatherAPI/opendata/opendata.php"
    "?dataType=SRS&year=2026&rformat=csv"
)

FILE = "Sun_rise_set_2026.csv"

HERE = Path(__file__).parent
DATA = HERE / "data"


def fetch(url, path):
    """Download the raw CSV once. If it already exists, do nothing."""

    if path.exists():
        print(
            f"data/{path.name} is already here "
            f"({path.stat().st_size // 1024} KB). "
            "Delete it if you want to fetch it again."
        )
        return path

    DATA.mkdir(exist_ok=True)

    print(f"asking {url}")

    reply = requests.get(
        url,
        timeout=60,
        headers={
            "User-Agent": "SD5913 PolyU student"
        }
    )

    reply.raise_for_status()

    # Save the original reply exactly as received.
    path.write_bytes(reply.content)

    print(
        f"saved data/{path.name} "
        f"({path.stat().st_size // 1024} KB)"
    )

    return path


if __name__ == "__main__":
    fetch(
        URL,
        DATA / FILE
    )