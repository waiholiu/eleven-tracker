# Eleven VR Online Player Tracker

A GitHub Actions workflow that scrapes [11clubhouse.com](https://11clubhouse.com/eleven-online-players.html) every 15 minutes and records the online player count (total + per country) to an Excel spreadsheet on OneDrive.

## Setup

### 1. Register an Azure AD App

1. Go to [Azure Portal → App registrations](https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps/ApplicationsListBlade)
2. Click **New registration**, name it (e.g. `eleven-tracker`), select **Accounts in this organizational directory only**
3. After creation, note the **Application (client) ID** and **Directory (tenant) ID**
4. Go to **Certificates & secrets → New client secret** — copy the secret value
5. Go to **API permissions → Add a permission → Microsoft Graph → Application permissions**
   - Add `Files.ReadWrite.All` and `User.Read.All`
6. Click **Grant admin consent** for your organization

### 2. Add GitHub Secrets

In this repo, go to **Settings → Secrets and variables → Actions** and add:

| Secret | Description |
|---|---|
| `AZURE_TENANT_ID` | Your Azure AD tenant ID |
| `AZURE_CLIENT_ID` | The app registration client ID |
| `AZURE_CLIENT_SECRET` | The client secret value |
| `ONEDRIVE_USER` | Your Microsoft account email (e.g. `user@contoso.com`) |
| `ONEDRIVE_FILE_PATH` | Path in OneDrive (default: `ElevenTracker/players.xlsx`) |

### 3. Run

The workflow runs automatically every 15 minutes, or trigger it manually from the **Actions** tab.

## Output

The spreadsheet has columns:

| Timestamp | Total Players | China | South Korea | Germany | ... |
|---|---|---|---|---|---|
| 2026-03-16 13:00:00 UTC | 271 | 71 | 14 | 12 | ... |

New country columns are added automatically when players from new countries appear.
