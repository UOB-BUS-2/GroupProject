import datetime
import os
import random

from datetime import datetime, timedelta

from app import app, db
from flask import render_template, current_app, redirect, url_for, flash, request
from app.models import User, Meal
from app.forms import LogMeal, LoginForm, RegistrationForm

from sqlalchemy.exc import IntegrityError
import sqlalchemy as sa
from flask_login import login_user, current_user, login_required, logout_user
from urllib.parse import urlsplit


@app.route("/", methods=["GET", "POST"])
# @login_required
def index():
    if current_user.is_authenticated:
        # defining the last 7 days cutoff for dashboard display of meals
        seven_days_ago = datetime.now().date() - timedelta(days=7)
        # retrieve the meals logged in last 7 days
        weekly_meals = [m for m in current_user.meals if m.date_added >= seven_days_ago]
        # sorting the meals to display, newest at the top
        display_meals = weekly_meals[::-1]
        # i've kept this in but currently not using
        last_7_meals = current_user.meals[-7:][::-1]
        protein_count = {}
        weekly_total = 0
        # swapped to using weekly meals, not just the last 7
        for meal in weekly_meals:
            weekly_total += meal.total_emissions
            # tally protein foods for the 'In the last week you had' card
            protein_count[meal.protein] = protein_count.get(meal.protein, 0) + 1

        sorted_protein_count = dict(
            sorted(protein_count.items(), key=lambda item: item[1],
                   reverse=True))  # just so it lists the protein count in the 'in the last week you had' in order of quantity (desc)
        # comparison logic, comparing to average person per number of meals
        num_meals = len(weekly_meals)
        comparison_delta = 0
        comparison_label = "lower"  # Default

        if num_meals > 0:
            # assuming avg person: 39kg/week for 21 meals
            expected = num_meals * (39.0 / 21)
            raw_percent = (weekly_total / expected) * 100

            # Calculate the difference from the 100% baseline
            comparison_delta = int(abs(100 - raw_percent))
            comparison_label = "higher" if raw_percent > 100 else "lower"

        return render_template("index.html",
                               meals_over_last_week=display_meals,
                               protein_count=sorted_protein_count,
                               weekly_total=weekly_total,
                               num_meals=num_meals,
                               comparison_delta=comparison_delta,
                               comparison_label=comparison_label,
                               user_name=current_user.username)
    else:
        return render_template("LandingPage.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))

    return render_template('SignupPage.html', title='Register', form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get(
            'next')  # this code is about redirecting users to a specific page they tried to access before logging in

        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('LoginPage.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/log_meal", methods=["GET", "POST"])
@login_required
def log_meal():
    seven_days_ago = datetime.now().date() - timedelta(days=7)

    # calc the rolling score for every user to find out current rank
    all_users = User.query.all()
    user_scores = []
    for u in all_users:
        u_rolling_score = sum(m.total_emissions for m in u.meals if m.date_added >= seven_days_ago)
        user_scores.append((u.username, u_rolling_score))

    # sorting scores (ascending) to find rank
    user_scores.sort(key=lambda x: x[1])

    # calc current user's specific rolling score
    emissions = sum(m.total_emissions for m in current_user.meals if m.date_added >= seven_days_ago)

    # find ranking in leaderboard
    rank = 0
    for i, (name, score) in enumerate(user_scores):
        if name == current_user.username:
            rank = i + 1
            break

    form = LogMeal()
    if form.validate_on_submit():
        if "None" in [form.carb_selected.data, form.protein_selected.data, form.veg_selected.data]:
            flash("You must select a food item from all 3 dropdown boxes.")
            return redirect(url_for("log_meal"))

        logged_meal = Meal(
            carb=form.carb_selected.data,
            protein=form.protein_selected.data,
            veg=form.veg_selected.data,
            user_id=current_user.id
        )
        logged_meal.calculate_emissions()

        current_user.weekly_score += logged_meal.total_emissions

        db.session.add(logged_meal)
        db.session.commit()
        return redirect(url_for('home_redirect', meal_id=logged_meal.id))

    return render_template("log_meal.html",
                           form=form,
                           rank=rank,
                           emissions=emissions,
                           user_name=current_user.username)


@app.route("/home_redirect/<meal_id>", methods=["GET", "POST"])
def home_redirect(meal_id):
    logged_meal = Meal.query.get(meal_id)

    total_emissions = logged_meal.total_emissions
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


@app.route("/leaderboard")
@login_required
def leaderboard():
    seven_days_ago = datetime.now().date() - timedelta(days=7)
    all_users = User.query.all()

    leaderboard_list = []
    for user in all_users:
        # only the meals in the last 7 days
        rolling_total = sum(m.total_emissions for m in user.meals if m.date_added >= seven_days_ago)
        leaderboard_list.append((user.username, rolling_total))

    # sort leaderboard by lowest score first
    leaderboard_list.sort(key=lambda x: x[1])

    return render_template('LeaderboardPage.html', usernames=leaderboard_list)
