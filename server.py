from flask import Flask, jsonify
from scraper import get_all_cases
import os

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"status": "OK", "message": "DropStrack scraper running"})

@app.route("/cases")
def cases():
    data = get_all_cases()
    return jsonify({
        "updated": __import__("time").time(),
        "cases": data
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
