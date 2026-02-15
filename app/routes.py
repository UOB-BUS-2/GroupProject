from app import app
from flask import render_template


@app.route("/",methods=["GET","POST"])
def index():
    return render_template("LandingPage.html")

@app.route("/signup",methods=["GET","POST"])
def signup():
    return render_template("SignupPage.html")

@app.route("/login",methods=["GET","POST"])
def login():
    return render_template("LoginPage.html")

@app.route("/home",methods=["GET","POST"])
def home():
    return render_template("HomePage.html")