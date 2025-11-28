# scraper.py
import requests
from bs4 import BeautifulSoup
import time

# Diccionario en memoria con los precios scrapeados
SCRAPED_DATA = {}

# Listado de cajas + URLs (ya cargado del archivo grande)
from boxes import CASES   # usamos boxes.py como archivo de listado

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def scrape_price(url):
    """Scrapea un precio de una caja desde su página del Market."""
    try:
        r = requests.get(url, headers=HEADERS, timeout=12)
        if r.status_code != 200:
            return "N/A"

        soup = BeautifulSoup(r.text, "html.parser")

        # Steam siempre muestra algo como:
        # "X for sale starting at $Y"
        text = soup.get_text(" ", strip=True)

        marker = "starting at $"
        if marker in text:
            value = text.split(marker)[-1].split(" ")[0]
            return f"${value}"

        return "N/A"
    except:
        return "N/A"


def scrape_all():
    """Scrapea TODAS las cajas y guarda los precios en SCRAPED_DATA."""
    global SCRAPED_DATA

    new_data = {}

    for item in CASES:
        name = item["name"]
        url = item["url"]

        print(f"[SCRAPER] Fetching: {name}")
        price = scrape_price(url)
        new_data[name] = price

        time.sleep(2)  # anti-rate-limit suave

    SCRAPED_DATA = new_data
    print("[SCRAPER] DONE")

    return new_data
