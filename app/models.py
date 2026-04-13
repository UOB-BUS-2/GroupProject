from datetime import date
from app import db, login
import sqlalchemy.orm as so
import sqlalchemy as sa
from flask import current_app
import csv
import os
from flask_login import UserMixin
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model,UserMixin):
    __tablename__ = 'users'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(63), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(119), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255))
    weekly_score: so.Mapped[int] = so.mapped_column(sa.Integer, index=True, default=0)

    meals: so.Mapped[list['Meal']] = so.relationship(back_populates='user')

    def get_leaderboard(self):
        leaderboard = []
        for user in User.query.all():
            leaderboard.append((user.weekly_score, user.username))
        leaderboard.sort()
        return leaderboard

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)




class Meal(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    carb: so.Mapped[str] = so.mapped_column(sa.String(16))
    protein: so.Mapped[str] = so.mapped_column(sa.String(16))
    veg: so.Mapped[str] = so.mapped_column(sa.String(16))
    total_emissions: so.Mapped[float] = so.mapped_column(sa.Float, default=0)
    date_added: so.Mapped[str] = so.mapped_column(sa.Date, default=date.today())

    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    user: so.Mapped[User] = so.relationship(back_populates='meals')

    def calculate_emissions(self):
        file_path = os.path.join(current_app.root_path, "static", "food_emissions_portions.csv")
        rows = []
        self.total_emissions = 0
        with open(file_path, "r") as file:
            reader = csv.reader(file, delimiter=",")
            for record in reader:
                rows.append(record)
        for row in rows:
            if row[0] == self.carb or row[0] == self.protein or row[0] == self.veg:
                self.total_emissions += float(row[5])

    def get_qualitative_impact(self):
        if self.total_emissions < 0.5:
            qualitative_impact = "very_low"
        elif self.total_emissions < 1:
            qualitative_impact = "low"
        elif self.total_emissions < 2:
            qualitative_impact = "medium"
        elif self.total_emissions < 3:
            qualitative_impact = "high"
        else:
            qualitative_impact = "very_high"
        return qualitative_impact

    def calculate_equivalent_miles(self):
        # Average car emits 0.4 kg CO2 per mile
        car_miles = round(self.total_emissions / 0.4, 1)
        return car_miles

    def __repr__(self):
        return f"{self.id}. {self.carb}, {self.protein}, {self.veg} - {self.total_emissions} - {self.date_added}"

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))