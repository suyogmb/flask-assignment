import os
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "flask_db")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "users")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]


@app.route("/", methods=["GET", "POST"])
def form():
    error = None
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        address = request.form.get("address", "").strip()

        if not name or not email or not address:
            error = "All fields are required."
            return render_template("form.html", error=error)

        try:
            collection.insert_one({"name": name, "email": email, "address": address})
            return redirect(url_for("success"))
        except PyMongoError as e:
            error = f"Database error: {str(e)}"

    return render_template("form.html", error=error)


@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True)
