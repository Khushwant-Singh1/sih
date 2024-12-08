from flask import Flask, render_template, request, redirect, flash
from flask_pymongo import PyMongo
from cryptography.fernet import Fernet
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

# MongoDB Atlas Configuration
app.config["MONGO_URI"] = "mongodb+srv://khushwant:qazwsxedc@cluster0.vtwkj.mongodb.net/"
mongo = PyMongo(app)

# Encryption Setup
key = Fernet.generate_key()
cipher_suite = Fernet(key)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        mac_address = request.form["mac_address"]
        switch_name = request.form["switch_name"]
        encryption_algo = request.form["encryption_algo"]
        ip_address = request.form["ip_address"]
        subnet_mask = request.form["subnet_mask"]

        # Encrypt the MAC Address
        encrypted_mac = cipher_suite.encrypt(mac_address.encode()).decode()

        # Save to MongoDB
        mongo.db.switches.insert_one({
            "mac_address": encrypted_mac,
            "switch_name": switch_name,
            "encryption_algo": encryption_algo,
            "ip_address": ip_address,
            "subnet_mask": subnet_mask
        })

        flash("Switch successfully added!", "success")
        return redirect("/")

    switches = mongo.db.switches.find()
    return render_template("index.html", switches=switches)

if __name__ == "__main__":
    app.run(debug=True)
