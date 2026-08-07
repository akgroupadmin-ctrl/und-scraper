import re
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


START_ID = 200
END_ID = 250

OUTPUT_FILE = "und_companies.xlsx"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0.0.0 Safari/537.36"
    )
}


results = []


def clean(text):
    if not text:
        return ""
    return re.sub(r"\s+", " ", text).strip()


def download(company_id):
    url = f"https://www.und.org.tr/firma-bilgileri/{company_id}"

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=20,
        )

        if response.status_code != 200:
            return None

        return response.text

    except Exception:
        return None
def parse_company(html, company_id):
    soup = BeautifulSoup(html, "lxml")

    company = ""
    h = soup.find(["h1", "h2", "h3"])

    if h:
        company = clean(h.get_text())

    address = ""
    city = ""
    country = ""
    phone = ""
    website = ""

    rows = soup.find_all("tr")

    for row in rows:

        cols = row.find_all(["td", "th"])

        if len(cols) < 2:
            continue

        key = clean(cols[0].get_text())
        value = clean(cols[1].get_text())

        if "Adres" in key:
            address = value

        elif "İl" in key:
            if "/" in value:
                parts = [x.strip() for x in value.split("/")]

                if len(parts) >= 2:
                    city = parts[0]
                    country = parts[1]
            else:
                city = value

        elif "Telefon" in key:
            phone = value

        elif "Website" in key:
            link = cols[1].find("a")

            if link:
                website = link.get("href", "").strip()
            else:
                website = value

    return {
        "ID": company_id,
        "Company": company,
        "Address": address,
        "City": city,
        "Country": country,
        "Phone": phone,
        "Website": website,
        "URL": f"https://www.und.org.tr/firma-bilgileri/{company_id}"
    }
def main():

    print(f"Scanning IDs {START_ID} - {END_ID}")

    for company_id in tqdm(range(START_ID, END_ID + 1)):

        html = download(company_id)

        if html is None:
            continue

        try:

            company = parse_company(html, company_id)

            if company["Company"]:
                results.append(company)

        except Exception as e:
            print(f"Error {company_id}: {e}")

        time.sleep(0.2)

    if not results:
        print("Nothing found.")
        return

    df = pd.DataFrame(results)

    df.to_excel(
        OUTPUT_FILE,
        index=False
    )

    print()
    print(f"Done! Saved {len(df)} companies.")
    print(f"File: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
