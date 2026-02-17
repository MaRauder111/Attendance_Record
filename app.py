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

    data[day_key] = time_value
    save_data(data)

    return jsonify({"day": day_key, "time": time_value})

@app.route("/history")
def history():
    return jsonify(load_data())

if __name__ == "__main__":
    app.run(debug=True)
