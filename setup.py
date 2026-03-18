from app.models import *
from app import db
def setup():
    db.drop_all()

    db.create_all()

    # Building the Leaderboard Users

    u1 = User(username='VKC', weekly_score=10)
    u1.set_password('12345')

    db.session.add(u1)
    db.session.commit()

    u2 = User(username='GG', weekly_score=5)
    u2.set_password('12345')

    db.session.add(u2)
    db.session.commit()

    u3 = User(username='EL', weekly_score=2)
    u3.set_password('12345')

    db.session.add(u3)
    db.session.commit()

