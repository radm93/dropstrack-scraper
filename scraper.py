import requests
import time
import json
from bs4 import BeautifulSoup

CASE_LIST = [ ... listado completo ... ]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "no-cache"
}

def get_price(case_name):
    url = f"https://steamcommunity.com/market/listings/730/{case_name.replace(' ', '%20')}"
    r = requests.get(url, headers=HEADERS, timeout=10)

    if r.status_code != 200:
        return "N/A"

    soup = BeautifulSoup(r.text, "html.parser")

    script_data = soup.find_all("script")

    for script in script_data:
        if "lowest_price" in script.text:
            text = script.text
            start = text.find('"lowest_price"')
            if start != -1:
                segment = text[start:start+120]
                price = segment.split(":")[1].split(",")[0].replace('"', '').strip()
                return price

    return "N/A"


def update_json():
    data = {"updated": int(time.time() * 1000), "cases": []}

    for case in CASE_LIST:
        price = get_price(case)
        data["cases"].append({
            "name": case,
            "price": price
        })
        time.sleep(2)

    with open("cases.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    update_json()
