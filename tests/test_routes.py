from app import app, db  # noqa: E402
from app.models import User  # noqa: E402


def _setup_only_allowed_users():
    # Mark app as testing mode.
    app.config["TESTING"] = True

    # Bypass @login_required on /leaderboard for this simple test.
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


def test_leaderboard():
    # Arrange: DB contains only viraj/james/george.
    _setup_only_allowed_users()

    # request the leaderboard page.
    client = app.test_client()
    resp = client.get("/leaderboard", follow_redirects=False) #obtain the response
    assert resp.status_code == 200 #200 status correct means a success

    # Assert: page renders and ordering is lowest emissions first.
    body = resp.get_data(as_text=True)
    assert "Leaderboard" in body
    assert body.index("george") < body.index("james")
    assert body.index("george") < body.index("viraj")