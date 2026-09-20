from pathlib import Path
from urllib.parse import quote_plus
import time
from playwright.sync_api import sync_playwright


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

QUERIES_FILE = BASE_DIR / "queries.txt"
AUTH_FILE = BASE_DIR / "auth_r.json"


# ============================================================
# LOAD QUERIES
# ============================================================

def load_queries():
    if not QUERIES_FILE.exists():
        raise FileNotFoundError(
            f"queries.txt not found: {QUERIES_FILE}"
        )

    with open(QUERIES_FILE, "r", encoding="utf-8") as f:
        return [
            line.strip()
            for line in f
            if line.strip()
        ]


# ============================================================
# MAIN
# ============================================================

def main():

    queries = load_queries()

    if not AUTH_FILE.exists():
        raise FileNotFoundError(
            f"auth.json not found: {AUTH_FILE}"
        )

    print(f"Loaded {len(queries)} queries")
    print(f"Using authentication state: {AUTH_FILE}")
    time.sleep(5)

    with sync_playwright() as p:

        # ----------------------------------------------------
        # Launch browser
        # ----------------------------------------------------

        browser = p.chromium.launch(
            headless=False
        )

        # ----------------------------------------------------
        # Create context using saved login session
        # ----------------------------------------------------

        context = browser.new_context(
            storage_state=str(AUTH_FILE)
        )
        time.sleep(5)
        page = context.new_page()

        # ----------------------------------------------------
        # Process queries
        # ----------------------------------------------------

        for index, query in enumerate(queries, start=1):

            url = (
                "https://www.bing.com/search"
                f"?q={quote_plus(query)}&qs=ds&form=QBRE"
            )

            print(
                f"\n[{index}/{len(queries)}] "
                f"Visiting: {url}"
            )

            try:

                page.goto(
                    url,
                    wait_until="domcontentloaded",
                    timeout=60000
                )

                print(f"Loaded: {query}")

                # Give the page a moment to finish rendering
                page.wait_for_timeout(3000)

                print(
                    f"Page title: {page.title()}"
                )
                time.sleep(5)

            except Exception as e:

                print(
                    f"ERROR processing '{query}': {e}"
                )

        # ----------------------------------------------------
        # Close everything
        # ----------------------------------------------------

        context.close()
        browser.close()

        print("\nAutomation completed.")


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
