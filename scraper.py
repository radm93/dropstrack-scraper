import requests
from bs4 import BeautifulSoup
from boxes import CASES

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def fetch_price(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        price_el = soup.select_one("#market_commodity_buyrequests span.normal_price")

        if not price_el:
            price_el = soup.select_one(".market_commodity_order_divider")

        if not price_el:
            return "N/A"

        text = price_el.get_text(strip=True)

        # Captura precios tipo:
        # "$1.23 USD"
        # "$0.87"
        # "Starting at: $13.26"
        import re
        match = re.search(r"\$([0-9]+\.[0-9]+)", text)
        if match:
            return f"${match.group(1)}"

        return "N/A"

    except Exception:
        return "N/A"


def get_all_cases():
    result = []

    for name, url in CASES:
        price = fetch_price(url)
        result.append({
            "name": name,
            "price": price
        })

    return result
