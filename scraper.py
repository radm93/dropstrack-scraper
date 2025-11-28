# scraper.py
import requests
from bs4 import BeautifulSoup
import time

SCRAPED_DATA = {}

from boxes import CASES

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

def extract_price_from_html(html):
    """
    Steam market devuelve varias formas posibles.
    Buscamos TODAS.
    """

    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(" ", strip=True)

    # Formato común:
    # "xxx for sale starting at $1.23"
    if "starting at $" in text:
        try:
            value = text.split("starting at $")[-1].split(" ")[0]
            return f"${value}"
        except:
            pass

    # Formato alternativo:
    # "Starting at: $1.23"
    if "Starting at: $" in text:
        try:
            value = text.split("Starting at: $")[-1].split(" ")[0]
            return f"${value}"
        except:
            pass

    # Formato raro que a veces devuelve Steam:
    for elem in soup.find_all("span"):
        if elem.text.strip().startswith("$"):
            return elem.text.strip()

    return "N/A"


def scrape_price(url):
    """Descarga HTML y extrae precio."""
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        if r.status_code != 200:
            print(f"[ERROR] Steam respondió {r.status_code} para {url}")
            return "N/A"

        return extract_price_from_html(r.text)

    except Exception as e:
        print("[ERROR]", e)
        return "N/A"


def scrape_all():
    """Scrapea TODAS las cajas y actualiza el dict global."""
    global SCRAPED_DATA

    print("[SCRAPER] Iniciando scraping…")
    new_data = {}

    for item in CASES:
        name = item["name"]
        url = item["url"]

        print(f"[SCRAPER] Fetching: {name}")
        price = scrape_price(url)
        new_data[name] = price

        time.sleep(1.5)  # Anti-baneo

    SCRAPED_DATA = {
        "updated": int(time.time() * 1000),
        "cases": [
            {"name": name, "price": price}
            for name, price in new_data.items()
        ]
    }

    print("[SCRAPER] COMPLETADO")
    return SCRAPED_DATA
