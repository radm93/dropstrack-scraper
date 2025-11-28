from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Scraper listo."

@app.route("/cases")
def cases():
    if not os.path.exists("cases.json"):
        return jsonify({"error": "Scraper not run yet"}), 500

    with open("cases.json", "r", encoding="utf8") as f:
        return jsonify(json.load(f))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
