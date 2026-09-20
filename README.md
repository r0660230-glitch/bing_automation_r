# Daily Bing Search Automation

A simple Playwright-based automation that runs daily through GitHub Actions and visits 15 Bing search URLs automatically.

## How It Works

```text
GitHub Actions
      ↓
Start temporary runner
      ↓
Install Python + Playwright + Chromium
      ↓
Read 15 queries from queries.txt
      ↓
Generate Bing search URLs
      ↓
Visit each Bing search URL
      ↓
Finish
      ↓
Runner is removed
```

No VPS or personal server is required.

## Project Structure

```text
bing-automation/
├── search.py
├── queries.txt
├── requirements.txt
└── .github/
    └── workflows/
        └── daily.yml
```

## Requirements

- GitHub account
- GitHub repository
- Python 3.11+
- Playwright
- Chromium
- Internet access

The GitHub Actions workflow installs Playwright and Chromium automatically, so you do not need to install them manually on your computer if you only run the automation through GitHub Actions.

## Setup

### 1. Create a GitHub repository

Create a repository and add these files:

- `search.py`
- `queries.txt`
- `requirements.txt`
- `.github/workflows/daily.yml`

### 2. Add your queries

Put one query per line in `queries.txt`.

Example:

```text
Discuss the structure and muscular system
What is artificial intelligence
Explain machine learning
What is cloud computing
Explain computer networks
What is database normalization
Explain operating systems
What is blockchain
Explain IoT
What is natural language processing
Explain neural networks
What is cybersecurity
Explain data structures
What is computer vision
What is deep learning
```

The script will process the queries one by one.

### 3. Run locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Install Chromium:

```bash
playwright install chromium
```

Run:

```bash
python search.py
```

## GitHub Actions

The workflow runs automatically every day.

Example schedule:

```yaml
on:
  schedule:
    - cron: "30 14 * * *"

  workflow_dispatch:
```

`30 14 * * *` means **2:30 PM UTC**, which is **8:00 PM IST**.

`workflow_dispatch` allows you to start the workflow manually from GitHub.

> GitHub Actions scheduled workflows can sometimes start a little later than the scheduled time.

## Example `search.py`

```python
from playwright.sync_api import sync_playwright
from urllib.parse import quote_plus


def load_queries():
    with open("queries.txt", "r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]


queries = load_queries()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    for query in queries:
        url = f"https://www.bing.com/search?q={quote_plus(query)}"

        print(f"Visiting: {url}")

        page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=60000
        )

        print(f"Loaded: {query}")

        page.wait_for_timeout(3000)

    browser.close()
```

## Example GitHub Actions Workflow

Create `.github/workflows/daily.yml`:

```yaml
name: Daily Bing Searches

on:
  schedule:
    - cron: "30 14 * * *"

  workflow_dispatch:

jobs:
  bing-search:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          playwright install chromium
          playwright install-deps chromium

      - name: Run Bing searches
        run: python search.py
```

## Important Notes

### No Personal Chrome Profile

The automation runs on the GitHub Actions runner. It does **not** use the Chrome profile on your personal computer.

```text
Your PC Chrome       ❌
GitHub runner        ✅
Playwright Chromium  ✅
```

### No Server Required

GitHub provides a temporary runner for the workflow.

```text
Start runner
    ↓
Run automation
    ↓
Visit 15 URLs
    ↓
Finish
    ↓
Runner removed
```

### Headless Mode

The example uses:

```python
headless=True
```

This means Chromium runs without displaying a visible browser window.

You will see the progress in the GitHub Actions logs.

## Testing

Before relying on the daily schedule:

1. Open your GitHub repository.
2. Go to **Actions**.
3. Select **Daily Bing Searches**.
4. Click **Run workflow**.
5. Open the running job.
6. Check the logs.

You should see output similar to:

```text
Visiting: https://www.bing.com/search?q=...
Loaded: Discuss the structure and muscular system

Visiting: https://www.bing.com/search?q=...
Loaded: What is artificial intelligence
```

## Customizing the Queries

To change the searches, simply edit:

```text
queries.txt
```

You do not need to change the Python code.

The automation can handle more or fewer queries, although this project is intended for 15 daily searches.

## License

This project is for personal/educational automation purposes.
