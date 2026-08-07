from playwright.sync_api import sync_playwright

URL = "https://www.und.org.tr/firma-bilgileri/10459"

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=True
    )

    page = browser.new_page(
        viewport={"width": 1600, "height": 3000}
    )

    page.goto(
        URL,
        wait_until="networkidle",
        timeout=60000
    )

    page.screenshot(
        path="page.png",
        full_page=True
    )

    with open("page.html", "w", encoding="utf-8") as f:
        f.write(page.content())

    browser.close()

print("DONE")
