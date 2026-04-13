from app import db
from app.models import *


def setup():
    db.create_all()

    u1 = User(username='Anthony', email="anthony@test.com")
    u1.set_password('hello')

    u2 = User(username='James', email="james@test.com")
    u2.set_password('hello')

    u3 = User(username='George', email="george@test.com")
    u3.set_password('hello')

    u4 = User(username='Ed', email="ed@test.com")
    u4.set_password('hello')

    u5 = User(username='Viraj', email="viraj@test.com")
    u5.set_password('hello')

    # m1 = Meal(
    #     carb="x",
    #     protein="y",
    #     veg="z",
    #     total_emissions=12,
    #     user_id=1
    # )
    #
    # m2 = Meal(
    #     carb="x",
    #     protein="y",
    #     veg="z",
    #     total_emissions=8,
    #     user_id=2
    # )
    #
    # m3 = Meal(
    #     carb="x",
    #     protein="y",
    #     veg="z",
    #     total_emissions=5,
    #     user_id=3
    # )
    #
    # m4 = Meal(
    #     carb="x",
    #     protein="y",
    #     veg="z",
    #     total_emissions=4.6,
    #     user_id=4
    # )

    instances = [u1, u2, u3, u4, u5]

    db.session.add_all(instances)
    db.session.commit()

