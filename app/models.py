from datetime import date
from app import db
import sqlalchemy.orm as so
import sqlalchemy as sa
from flask import current_app
import csv
import os

class User:
    def __init__(self, username):
        self.username = username
        self.logged_meals = []

class Meal(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    carb: so.Mapped[str] = so.mapped_column(sa.String(16))
    protein: so.Mapped[str] = so.mapped_column(sa.String(16))
    veg: so.Mapped[str] = so.mapped_column(sa.String(16))
    total_emissions: so.Mapped[float] = so.mapped_column(sa.Float, default=0)
    date_added: so.Mapped[str] = so.mapped_column(sa.Date, default=date.today())

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