import os
import random
import csv
from app import app
from flask import render_template, current_app, redirect, url_for
from app.models import User, Meal
from app.forms import LogMeal
from app.forms import LogFood

# EMISSIONS_DATA = "app/data/food_emissions_portions.csv"
#
# foods_by_category = {}
# co2_by_food = {}
#
# with open(EMISSIONS_DATA, newline="") as f:
#
#     rows = csv.DictReader(f)
#
#     for row in rows:
#
#         category = row["Category"].strip()
#         food = row["Food"].strip()
#         co2 = float(row["CO2 per Portion (kg)"])
#
#         if category not in foods_by_category:
#             foods_by_category[category] = []
#         foods_by_category[category].append(food)
#         co2_by_food[food] = co2
#
# categories = sorted(foods_by_category.keys())
#
# @app.route("/", methods=["GET", "POST"])
# def log_food():
#
#     form = LogFood()
#
#     form.category.choices = [(c, c) for c in categories]
#     selected_category = form.category.data or categories[0]
#     foods = foods_by_category[selected_category]
#     form.food.choices = [(f, f) for f in foods]
#
#     result = None
#
#     if form.validate_on_submit():
#
#         food = form.food.data
#         portions = form.portions.data
#         result = round(portions * co2_by_food[food], 4)
#
#     return render_template(
#         "log_food.html",
#         form=form,
#         result=result
#     )

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
        logged_meal = Meal(form.carb_selected.data, form.protein_selected.data, form.veg_selected.data)
        return redirect(url_for('home_redirect', logged_meal=logged_meal))

    return render_template("log_meal.html", form=form)




@app.route("/home_redirect/<logged_meal>", methods=["GET","POST"])
def home_redirect(logged_meal):
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

@app.route("/leaderboard", methods = ['GET', 'POST'])
def leaderboard():

    return render_template('LeaderboardPage.html')