from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    context = browser.new_context()
    page = context.new_page()

    page.goto("https://www.bing.com")

    input("Log in manually, then press ENTER here...")

    context.storage_state(path="auth_p.json")

    print("Login session saved to auth_p.json")

    browser.close()