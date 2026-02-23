import os
import random
from app import app
from flask import render_template, current_app
from app.classes import User, Meal


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


@app.route("/home_redirect/<meal_object>", methods=["GET","POST"])
def home_redirect(meal_object):
    total_emissions = None
    qualitative_impact = "low"
    car_miles = None

    file_path = os.path.join(current_app.root_path, "static", "generic_tips.txt")
    random_line = random.randint(0, 29)
    with open(file_path, "r") as file:
        tips = file.readlines()
    generic_tip = tips[random_line]

    return render_template("HomeRedirect.html",
                           total_emissions=total_emissions,
                           qualitative_impact=qualitative_impact,
                           car_miles=car_miles,
                           generic_tip=generic_tip)