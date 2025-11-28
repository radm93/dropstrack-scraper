import json
import time
import requests
import re
from boxes import BOXES

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

PRICE_RE = re.compile(r'"lowest_price":"([^"]+)"')

def scrape(url):
    try:
        html = requests.get(url, headers=HEADERS, timeout=6).text
        m = PRICE_RE.search(html)
        if not m:
            return "N/A"
        return m.group(1)
    except:
        return "N/A"

def run_scraper():
    data = []
    for name, url in BOXES.items():
        print("Scraping:", name)
        price = scrape(url)
        data.append({"name": name, "price": price})
        time.sleep(1)

    with open("cases.json", "w", encoding="utf8") as f:
        json.dump({
            "updated": int(time.time()*1000),
            "cases": data
        }, f, indent=2)

if __name__ == "__main__":
    run_scraper()
