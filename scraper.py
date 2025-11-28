# scraper.py
import re
import requests
import time
from boxes import CASES

SCRAPED_DATA = {}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def scrape_price(url):
    """
    Extrae precio desde el JSON interno de Steam, evitando el texto del HTML completo.
    """
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)

        if r.status_code != 200:
            return "N/A"

        html = r.text

        # Steam siempre incluye este JSON:
        # "lowest_price":"$1.23"
        match = re.search(r'"lowest_price":"([^"]+)"', html)
        if match:
            return match.group(1)

        return "N/A"

    except Exception as e:
        print("ERROR:", e)
        return "N/A"


def scrape_all():
    """
    Scrapea todas las cajas y actualiza SCRAPED_DATA.
    Nunca explota, nunca cuelga el worker.
    """
    global SCRAPED_DATA

    print("[SCRAPER] Starting…")

    result = {
        "updated": int(time.time() * 1000),
        "cases": []
    }

    for item in CASES:
        name = item["name"]
        url = item["url"]

        print(f"[SCRAPER] {name}")

        price = scrape_price(url)
        result["cases"].append({
            "name": name,
            "price": price
        })

        time.sleep(1)  # seguro para Railway

    SCRAPED_DATA = result
    print("[SCRAPER] DONE")
    return SCRAPED_DATA
