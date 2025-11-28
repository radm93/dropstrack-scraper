from flask import Flask, jsonify
from scraper import get_all_cases

app = Flask(__name__)

@app.route("/cases")
def cases():
    data = get_all_cases()
    return jsonify({
        "updated": __import__("time").time(),
        "cases": data
    })

@app.route("/")
def home():
    return jsonify({"status": "OK", "message": "DropStrack scraper running"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
