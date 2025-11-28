import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9",
}

CASE_URLS = {
    "Revolution Case": "https://steamcommunity.com/market/listings/730/Revolution%20Case",
    "Kilowatt Case": "https://steamcommunity.com/market/listings/730/Kilowatt%20Case",
    "Recoil Case": "https://steamcommunity.com/market/listings/730/Recoil%20Case"
}

def get_price(url):
    try:
        html = requests.get(url, headers=HEADERS, timeout=10).text
        soup = BeautifulSoup(html, "lxml")

        price_el = soup.select_one(".market_listing_price.market_listing_price_with_fee")
        if not price_el:
            return "N/A"

        return price_el.get_text(strip=True)
    except:
        return "N/A"

def fetch_case_prices():
    result = []

    for name, url in CASE_URLS.items():
        price = get_price(url)
        result.append({"name": name, "price": price})

    return {"cases": result}
