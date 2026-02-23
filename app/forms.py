from random import choice

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.fields.choices import SelectField, SelectMultipleField
from wtforms.fields.simple import BooleanField, PasswordField
from wtforms.validators import DataRequired, Length
from datetime import date

from wtforms.widgets.core import CheckboxInput


class LogMeal(FlaskForm):
    # Maybe added later
    #meal_of_day = SelectField("Log a meal", validators=[DataRequired()], choices = [('breakfast', 'Breakfast'), ('lunch', 'Lunch'), ('dinner', 'Dinner'), ('snack', 'Snack')])
    protein_selected = SelectField("What was your main source of protein", validators=[DataRequired('Please make a selection')],default = None,
                                         choices=[(None, '--- Select Protein ---'), ('beef', 'Beef'),('chicken', 'Chicken'),('eggs', 'Eggs'),('tofu', 'Tofu'), ('fish', 'Fish and seafood')])
    carb_selected = SelectField("What was your main carbohydrate", validators=[DataRequired()],default = None,
                                         choices=[(None, '--- Select Carbohydrate ---'), ('bread', 'Bread'),('rice', 'Rice'),('pasta', 'Pasta')])
    veg_selected = SelectField("What was your main vegetable", validators=[DataRequired()], default = None,
                                         choices=[(None, '--- Select Vegetable ---'), ('potato', 'Potato'),('carrot', 'Carrot'),('broccoli', 'Broccoli'),('spinach', 'Spinach'), ('onion', 'Onion')])
    # Maybe added later
    # date_completed = DateField(
    #     "When did you have this?",
    #     format="%Y-%m-%d",
    #     default=date.today
    # )
    submit = SubmitField("Submit Meal")