# server.py
from flask import Flask, jsonify
import threading
from scraper import SCRAPED_DATA, scrape_all

app = Flask(__name__)

@app.route("/")
def home():
    return "DropStrack CS2 Scraper is running."

@app.route("/cases")
def get_cases():
    """Retorna los precios ya scrapeados."""
    return jsonify(SCRAPED_DATA)

@app.route("/refresh")
def refresh():
    """Inicia scraping en segundo plano."""
    thread = threading.Thread(target=scrape_all)
    thread.start()
    return jsonify({"status": "Scraping started"})


if __name__ == "__main__":
    # No bloqueamos el arranque con scraping
    app.run(host="0.0.0.0", port=8080)
