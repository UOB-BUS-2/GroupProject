from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, DateField, FloatField,
                     SelectField, PasswordField, BooleanField)
from wtforms.validators import DataRequired, Length

from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from datetime import date

from app.models import User
from app import db
import sqlalchemy as sa

class LogMeal(FlaskForm):
    # Maybe added later
    #meal_of_day = SelectField("Log a meal", validators=[DataRequired()], choices = [('breakfast', 'Breakfast'), ('lunch', 'Lunch'), ('dinner', 'Dinner'), ('snack', 'Snack')])
    protein_selected = SelectField("What was your main source of protein", validators=[DataRequired('Please make a selection')],default = None,
                                         choices=[(None, '--- Select Protein ---'), ('beef', 'Beef'),('chicken', 'Chicken'),('eggs', 'Eggs'),('tofu', 'Tofu'), ('fish', 'Fish and seafood')])
    carb_selected = SelectField("What was your main carbohydrate", validators=[DataRequired()],default = None,
                                         choices=[(None, '--- Select Carbohydrate ---'), ('bread', 'Bread'),('rice', 'Rice'),('pasta', 'Pasta')])
    veg_selected = SelectField("What was your main vegetable", validators=[DataRequired()], default = None,
                                         choices=[(None, '--- Select Vegetable ---'), ('potato', 'Potato'),('carrot', 'Carrot'),('broccoli', 'Broccoli'),('tomato', 'Tomato'), ('onion', 'Onion')])
    # Maybe added later
    # date_completed = DateField(
    #     "When did you have this?",
    #     format="%Y-%m-%d",
    #     default=date.today
    # )

    # ignore this line, testing a push
    submit = SubmitField("Submit Meal")

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(
            User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(
            User.email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email address.')