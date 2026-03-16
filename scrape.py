"""
Scrapes https://11clubhouse.com/eleven-online-players.html for online player counts
and appends a timestamped row to a local Excel file (committed back to the repo).
"""

import os
import re
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook, load_workbook

SCRAPE_URL = "https://11clubhouse.com/eleven-online-players.html"
XLSX_PATH = Path("data/players.xlsx")


def scrape_players() -> dict:
    """Scrape the page and return total + per-country player counts."""
    resp = requests.get(SCRAPE_URL, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # Total players from the <h2> heading, e.g. "262 players online right now !"
    h2 = soup.find("h2", class_="title_shadow")
    total_match = re.search(r"(\d+)\s+players?\s+online", h2.get_text() if h2 else "")
    total = int(total_match.group(1)) if total_match else 0

    # Country data from title attributes like 'China: 70 users online'
    countries = {}
    for link in soup.select("ol.list_pays li a.tooltipgo"):
        title = link.get("title", "")
        m = re.match(r"(.+?):\s*(\d+)\s+users?\s+online", title)
        if m:
            countries[m.group(1)] = int(m.group(2))

    return {"total": total, "countries": countries}


def build_row(timestamp: str, data: dict, all_countries: list[str]) -> list:
    """Build a spreadsheet row: [timestamp, total, country1, country2, ...]."""
    row = [timestamp, data["total"]]
    for c in all_countries:
        row.append(data["countries"].get(c, 0))
    return row


def main():
    print("Scraping player data...")
    data = scrape_players()
    print(f"  Total: {data['total']} players, {len(data['countries'])} countries")

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    XLSX_PATH.parent.mkdir(parents=True, exist_ok=True)

    if XLSX_PATH.exists():
        wb = load_workbook(XLSX_PATH)
        ws = wb.active
    else:
        print("  No existing file — creating new spreadsheet.")
        wb = Workbook()
        ws = wb.active
        ws.title = "Player Counts"
        all_countries = sorted(data["countries"].keys())
        headers = ["Timestamp", "Total Players"] + all_countries
        ws.append(headers)

    # Determine existing country columns from the header row
    header_row = [cell.value for cell in ws[1]]
    existing_countries = header_row[2:]

    # Add any new countries not yet in the header
    new_countries = sorted(set(data["countries"].keys()) - set(existing_countries))
    if new_countries:
        print(f"  Adding {len(new_countries)} new country columns: {new_countries}")
        for c in new_countries:
            existing_countries.append(c)
            ws.cell(row=1, column=len(existing_countries) + 2, value=c)

    row = build_row(timestamp, data, existing_countries)
    ws.append(row)

    wb.save(XLSX_PATH)
    print(f"Done! Row added at {timestamp} → {XLSX_PATH}")


if __name__ == "__main__":
    main()
