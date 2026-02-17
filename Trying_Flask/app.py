from flask import Flask, render_template, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

DATA_FILE = "timestamps.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/save", methods=["POST"])
def save_timestamp():
    data = load_data()

    now = datetime.now()
    day_key = now.strftime("%Y-%m-%d")
    time_value = now.strftime("%H:%M:%S")

    if day_key in data:
        return jsonify({
            "status": "exists",
            "day": day_key,
            "time": data[day_key]
        })

    data[day_key] = time_value
    save_data(data)

    return jsonify({
        "status": "saved",
        "day": day_key,
        "time": time_value
    })

@app.route("/history")
def history():
    return jsonify(load_data())

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
