import json
import os
from flask import Flask, jsonify

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")


@app.route("/api", methods=["GET"])
def get_data():
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
