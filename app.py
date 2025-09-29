import os
from flask import Flask, render_template, request, redirect, session, url_for
import pyrebase
import firebase_admin
from firebase_admin import credentials, auth
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# Firebase config
firebase_config = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "databaseURL": os.getenv("FIREBASE_DATABASE_URL"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": os.getenv("FIREBASE_APP_ID"),
    "measurementId": os.getenv("FIREBASE_MEASUREMENT_ID")
}

# Initialize Pyrebase
firebase = pyrebase.initialize_app(firebase_config)
pb_auth = firebase.auth()

# Initialize Firebase Admin SDK
print("FIREBASE_SERVICE_ACCOUNT:", os.getenv("FIREBASE_SERVICE_ACCOUNT"))
cred = credentials.Certificate(os.getenv("FIREBASE_SERVICE_ACCOUNT"))
firebase_admin.initialize_app(cred)


@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        try:
            pb_auth.create_user_with_email_and_password(email, password)
            return redirect(url_for("login"))
        except Exception as e:
            return render_template("register.html", error=str(e))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        try:
            pb_auth.sign_in_with_email_and_password(email, password)
            session["user"] = email
            return redirect(url_for("dashboard"))
        except Exception as e:

            error_json = e.args[1]  
            error = json.loads(error_json)  
            message = error["error"]["message"]  

            return render_template("login.html", error=str(message))
        
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    users = [u.email for u in auth.list_users().iterate_all()]
    return render_template("dashboard.html", user=session["user"], users=users)


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")
