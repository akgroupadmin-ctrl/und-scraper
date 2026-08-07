from playwright.sync_api import sync_playwright


URL = "https://www.und.org.tr/firma-bilgileri/10459"


with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=True
    )

    page = browser.new_page()

    page.goto(
        URL,
        wait_until="networkidle",
        timeout=60000
    )

    page.screenshot(path="page.png", full_page=True)

    html = page.content()

    with open("page.html", "w", encoding="utf-8") as f:
        f.write(html)

    browser.close()

print("DONE")
