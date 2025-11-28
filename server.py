from flask import Flask, jsonify
import threading
import time
import requests
from bs4 import BeautifulSoup
import json
import os

app = Flask(__name__)

# Archivo donde guardamos los datos del scrapeo
CACHE_FILE = "cases.json"

# Lista de cajas -> LINK REAL
CASES = {
    "Revolution Case": "https://steamcommunity.com/market/listings/730/Revolution%20Case",
    "Kilowatt Case": "https://steamcommunity.com/market/listings/730/Kilowatt%20Case",
    "Recoil Case": "https://steamcommunity.com/market/listings/730/Recoil%20Case",
    "Dreams & Nightmares Case": "https://steamcommunity.com/market/listings/730/Dreams%20%26%20Nightmares%20Case",
    "Snakebite Case": "https://steamcommunity.com/market/listings/730/Snakebite%20Case",
    "Operation Broken Fang Case": "https://steamcommunity.com/market/listings/730/Operation%20Broken%20Fang%20Case",
    "Fracture Case": "https://steamcommunity.com/market/listings/730/Fracture%20Case",
    "Prisma Case": "https://steamcommunity.com/market/listings/730/Prisma%20Case",
    "Prisma 2 Case": "https://steamcommunity.com/market/listings/730/Prisma%202%20Case",
    "Horizon Case": "https://steamcommunity.com/market/listings/730/Horizon%20Case",
    "Danger Zone Case": "https://steamcommunity.com/market/listings/730/Danger%20Zone%20Case",
    "Clutch Case": "https://steamcommunity.com/market/listings/730/Clutch%20Case",
    "Spectrum Case": "https://steamcommunity.com/market/listings/730/Spectrum%20Case",
    "Spectrum 2 Case": "https://steamcommunity.com/market/listings/730/Spectrum%202%20Case",
    "Glove Case": "https://steamcommunity.com/market/listings/730/Glove%20Case",
    "Chroma Case": "https://steamcommunity.com/market/listings/730/Chroma%20Case",
    "Chroma 2 Case": "https://steamcommunity.com/market/listings/730/Chroma%202%20Case",
    "Chroma 3 Case": "https://steamcommunity.com/market/listings/730/Chroma%203%20Case",
    "Falchion Case": "https://steamcommunity.com/market/listings/730/Falchion%20Case",
    "Gamma Case": "https://steamcommunity.com/market/listings/730/Gamma%20Case",
    "Gamma 2 Case": "https://steamcommunity.com/market/listings/730/Gamma%202%20Case",
    "Shadow Case": "https://steamcommunity.com/market/listings/730/Shadow%20Case",
    "Huntsman Weapon Case": "https://steamcommunity.com/market/listings/730/Huntsman%20Weapon%20Case",
    "Operation Phoenix Weapon Case": "https://steamcommunity.com/market/listings/730/Operation%20Phoenix%20Weapon%20Case",
    "Operation Breakout Weapon Case": "https://steamcommunity.com/market/listings/730/Operation%20Breakout%20Weapon%20Case",
    "Operation Wildfire Case": "https://steamcommunity.com/market/listings/730/Operation%20Wildfire%20Case",
    "Operation Hydra Case": "https://steamcommunity.com/market/listings/730/Operation%20Hydra%20Case",
    "Operation Vanguard Weapon Case": "https://steamcommunity.com/market/listings/730/Operation%20Vanguard%20Weapon%20Case",
    "Operation Bravo Case": "https://steamcommunity.com/market/listings/730/Operation%20Bravo%20Case",
    "CS20 Case": "https://steamcommunity.com/market/listings/730/CS20%20Case",
    "CS:GO Weapon Case": "https://steamcommunity.com/market/listings/730/CS%3AGO%20Weapon%20Case",
    "CS:GO Weapon Case 2": "https://steamcommunity.com/market/listings/730/CS%3AGO%20Weapon%20Case%202",
    "CS:GO Weapon Case 3": "https://steamcommunity.com/market/listings/730/CS%3AGO%20Weapon%20Case%203",
    "Winter Offensive Weapon Case": "https://steamcommunity.com/market/listings/730/Winter%20Offensive%20Weapon%20Case",
    "Revolver Case": "https://steamcommunity.com/market/listings/730/Revolver%20Case",
    "Gallery Case": "https://steamcommunity.com/market/listings/730/Gallery%20Case",
    "Sealed Genesis Terminal": "https://steamcommunity.com/market/listings/730/Sealed%20Genesis%20Terminal",
    "Fever Case": "https://steamcommunity.com/market/listings/730/Fever%20Case",
    "X-Ray P250 Package": "https://steamcommunity.com/market/listings/730/X-Ray%20P250%20Package",
    "eSports 2013 Case": "https://steamcommunity.com/market/listings/730/eSports%202013%20Case",
    "eSports 2013 Winter Case": "https://steamcommunity.com/market/listings/730/eSports%202013%20Winter%20Case",
    "eSports 2014 Summer Case": "https://steamcommunity.com/market/listings/730/eSports%202014%20Summer%20Case"
}


def scrape_price(url):
    """Scrapea una página de Steam y devuelve el precio."""
    try:
        r = requests.get(url, timeout=12, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(r.text, "html.parser")

        el = soup.select_one("#market_commodity_forsale > span.market_commodity_orders_header_promote")
        if not el:
            return "N/A"

        txt = el.text.strip()
        if "Starting at" in txt or "starting at" in txt:
            price = txt.split("$")[-1]
            return f"${price}"

        return "N/A"

    except:
        return "N/A"


def run_scraper():
    print("🔄 Ejecutando SCRAPER en segundo plano...")

    results = []

    for name, url in CASES.items():
        print(f"Scrapeando → {name}")
        price = scrape_price(url)
        results.append({"name": name, "price": price})
        time.sleep(1)  # evita bloqueo de Steam

    data = {"updated": int(time.time() * 1000), "cases": results}

    with open(CACHE_FILE, "w") as f:
        json.dump(data, f)

    print("✅ SCRAPER COMPLETADO. Datos guardados.")


@app.route("/cases")
def serve_cases():
    """Responde INSTANTÁNEO con el último cache."""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE) as f:
            return jsonify(json.load(f))
    else:
        return jsonify({"status": "Scraper still running..."})


@app.route("/refresh")
def refresh():
    """Dispara el scraper en segundo plano."""
    threading.Thread(target=run_scraper).start()
    return jsonify({"status": "Scraper started"})


@app.route("/")
def root():
    return jsonify({"status": "OK", "message": "Scraper running"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
