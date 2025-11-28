from flask import Flask, jsonify
import threading
from scraper import SCRAPED_DATA, scrape_all

app = Flask(__name__)

@app.route("/")
def home():
    return "DropStrack CS2 Scraper is running."

@app.route("/cases")
def get_cases():
    return jsonify(SCRAPED_DATA)

@app.route("/refresh")
def refresh():
    thread = threading.Thread(target=scrape_all)
    thread.start()
    return jsonify({"status": "Scraping started"})

# ❗ NO USAR app.run() EN RAILWAY
# Gunicorn ejecutará esto automáticamente
