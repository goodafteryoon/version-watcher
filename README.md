# Chrome Extension Version Watcher

This project automatically monitors the version of a Chrome extension (or any web resource exposing a version) and sends a Slack notification when a new version is detected.

## Features

- Periodically checks the target web page for version updates using Selenium and Chromium.
- Notifies a Slack channel via webhook when a new version is found.
- Stores the last detected version to avoid duplicate notifications.
- Fully automated with GitHub Actions (runs every 5 minutes by default).

## Requirements

- Python 3.x
- Chrome/Chromium and ChromeDriver
- Slack Incoming Webhook URL
- The target URL where the version information is displayed

## Installation

1. Clone this repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set environment variables (you can use a `.env` file):
   ```
   SLACK_WEBHOOK_URL=your_slack_webhook_url
   URL=the_url_to_check
   ```

## Usage

To run the version checker locally:

```bash
python check_version.py
```

## How It Works

- The script uses Selenium to open the target URL in headless Chromium.
- It searches for a div containing "버전" or "Version" and extracts the following sibling div's text as the version.
- If the version has changed since the last check, it sends a notification to Slack and updates the local record.

## GitHub Actions

This project includes a GitHub Actions workflow that:

- Runs every 5 minutes (configurable via cron).
- Installs dependencies and Chromium/ChromeDriver.
- Runs the version checker script.
- Requires the following secrets to be set in your repository:
  - `SLACK_WEBHOOK_URL`
  - `URL`

## File Structure

- `check_version.py` — Main script for version checking and notification.
- `requirements.txt` — Python dependencies.
- `.github/workflows/check_version.yml` — GitHub Actions workflow for automation.

## Customization

- Adjust the XPATH in `check_version.py` if your version element is located differently.
- Change the Slack message format as needed.
