import os
import random

from app import app, db
from flask import render_template, current_app, redirect, url_for
from app.models import User, Meal
from app.forms import LogMeal


@app.route("/",methods=["GET","POST"])
def index():
    return render_template("LandingPage.html")


@app.route("/signup",methods=["GET","POST"])
def signup():
    return render_template("SignupPage.html")


@app.route("/login",methods=["GET","POST"])
def login():
    return render_template("LoginPage.html")


@app.route("/log_meal",methods=["GET","POST"])
def log_meal():
    form = LogMeal()
    if form.validate_on_submit():
        logged_meal = Meal(
            carb=form.carb_selected.data,
            protein=form.protein_selected.data,
            veg=form.veg_selected.data
        )
        logged_meal.calculate_emissions()
        db.session.add(logged_meal)
        db.session.commit()
        return redirect(url_for('home_redirect', meal_id=logged_meal.id))
    return render_template("log_meal.html", form=form)


@app.route("/home_redirect/<meal_id>", methods=["GET","POST"])
def home_redirect(meal_id):
    logged_meal = Meal.query.get(meal_id)

    total_emissions = round(logged_meal.total_emissions, 3)
    qualitative_impact = logged_meal.get_qualitative_impact()
    car_miles = logged_meal.calculate_equivalent_miles()

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


@app.route("/leaderboard", methods = ['GET', 'POST'])
def leaderboard():
    return render_template('LeaderboardPage.html')