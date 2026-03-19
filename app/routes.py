import os
import random

from app import app, db
from flask import (render_template, current_app, redirect, url_for, flash,
                   request)
from app.models import User, Meal
from app.forms import LogMeal, LoginForm, RegistrationForm

from sqlalchemy.exc import IntegrityError
import sqlalchemy as sa
from flask_login import login_user, current_user, login_required, logout_user
from urllib.parse import urlsplit


@app.route("/",methods=["GET","POST"])
@login_required
def index():
    return render_template("LandingPage.html")


@app.route("/signup",methods=["GET","POST"])
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


@app.route("/login",methods=["GET","POST"])
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
        next_page = request.args.get('next') # this code is about redirecting users to a specific page they tried to access before logging in

        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('LoginPage.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


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


@app.route("/leaderboard")
@login_required
def leaderboard():
    users = db.session.query(User.username, User.weekly_score)\
        .order_by(User.weekly_score.desc())\
        .all()

    return render_template('LeaderboardPage.html', usernames=users)