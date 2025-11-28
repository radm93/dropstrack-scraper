from flask import Flask, jsonify
from scraper import fetch_case_prices

app = Flask(__name__)

@app.route("/")
def home():
    return "Dropstrack Scraper Running"

@app.route("/cases")
def cases():
    return jsonify(fetch_case_prices())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
