# Eleven VR Online Player Tracker

A GitHub Actions workflow that scrapes [11clubhouse.com](https://11clubhouse.com/eleven-online-players.html) every 15 minutes and records the online player count (total + per country) to an Excel spreadsheet committed to this repo.

## Setup

No secrets or API keys needed — it just works!

To sync to OneDrive, clone this repo into your OneDrive folder:
```bash
cd "C:\Users\YourName\OneDrive"
git clone https://github.com/waiholiu/eleven-tracker.git
```
Then run `git pull` periodically (or set up a scheduled task) to keep `data/players.xlsx` in sync.

## Manual Trigger

Go to the **Actions** tab → **Scrape Eleven VR Online Players** → **Run workflow**.

## Output

The spreadsheet (`data/players.xlsx`) has columns:

| Timestamp | Total Players | China | South Korea | Germany | ... |
|---|---|---|---|---|---|
| 2026-03-16 13:00:00 UTC | 271 | 71 | 14 | 12 | ... |

New country columns are added automatically when players from new countries appear.
