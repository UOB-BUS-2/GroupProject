"""
Run tests with

- pip install pytest

- from root project just run : pytest


"""


from app import app, db
from app.models import User, Meal


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
        db.session.flush()
        # Updated: log meals so leaderboard has data to calculate
        # george with lowst emission meal, james and viraj both with high emission meals
        m_george = Meal(protein="beans", carb="pasta", veg="tomato", user_id=u3.id)
        m_george.calculate_emissions()  # gives george lowest score of the three

        # James & Viraj - high emission meals
        m_james = Meal(protein="beef", carb="pasta", veg="tomato", user_id=u2.id)
        m_james.calculate_emissions()  # Sets high score

        m_viraj = Meal(protein="beef", carb="pasta", veg="tomato", user_id=u1.id)
        m_viraj.calculate_emissions()

        db.session.add_all([m_george, m_james, m_viraj])
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

# check that the pages don't crash
def test_about_page_loads():
    client = app.test_client()
    response = client.get("/about")
    assert response.status_code == 200
    assert b"About" in response.data