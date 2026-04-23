"""
Run tests with

- pip install pytest

- from root project just run : pytest


"""


from app import app, db
from app.models import User


def setup_only_allowed_users():
    # Mark app as testing mode.
    app.config["TESTING"] = True #this enables testing mode in Flask for us -

    # Bypass @login_required on /leaderboard so can test the leaderboard solely
    app.config["LOGIN_DISABLED"] = True

    with app.app_context():
        # Ensure the DB contains ONLY the allowed users.
        db.drop_all()
        db.create_all()

        u1 = User(username="viraj", email="virajkc1@example.com", weekly_score=10)
        u1.set_password("hello")

        u2 = User(username="james", email="high@example.com", weekly_score=10)
        u2.set_password("hello")

        u3 = User(username="george", email="mid@example.com", weekly_score=5)
        u3.set_password("hello")

        db.session.add_all([u1, u2, u3])
        db.session.commit()

"""
Tests order of leaderboard is

george = 5
james = 10
viraj = 10

"""
def test_leaderboard():
    # Arrange: DB contains only viraj/james/george. - NOTE it uses our actual database
    setup_only_allowed_users() ##creates and adds the users in database with these scores

    # request the leaderboard page.
    client = app.test_client() #IMPORTANT - this line essentially creates  a test client - simulates HTTP reqs w/o an actual server
    resp = client.get("/leaderboard", follow_redirects=False) #obtain the response after client runs /leaderboard no redirects are allowed so solely tests leaderboard
    assert resp.status_code == 200 #200 status correct means a success - assert checks correct status code

    # Assert: page renders and ordering is lowest emissions first.
    body = resp.get_data(as_text=True) # get_data just converts response into a string
    assert "Leaderboard" in body #checks code renders
    #THESE ARE THE TESTS RUNNING
    assert body.index("george") < body.index("james") # .index is the position  so just checking in the html george is before  james
    assert body.index("george") < body.index("viraj")