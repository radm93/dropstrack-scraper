from flask import Flask, jsonify
from scraper import get_all_cases
import os

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"status": "running"})

@app.route("/cases")
def list_cases():
    return jsonify({
        "updated": __import__("time").time(),
        "cases": get_all_cases()
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
