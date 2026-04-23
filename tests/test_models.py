from app import app, db
from app.models import User


def _setup_only_allowed_users():
    # Use the test database fresh for this test run.
    app.config["TESTING"] = True

    # Build a clean schema so there are no leftover users from app.db.
    with app.app_context():
        db.drop_all() #basically a test database clearing the table and creating a new one per run
        db.create_all()

        # Only allowed test users to test the leadrboard
        u1 = User(username="viraj", email="virajkc1@example.com", weekly_score=10)
        u1.set_password("hello")

        u2 = User(username="james", email="high@example.com", weekly_score=10)
        u2.set_password("hello")

        u3 = User(username="george", email="mid@example.com", weekly_score=5)
        u3.set_password("hello")

        # Save users so the leaderboard query can find them.
        db.session.add_all([u1, u2, u3])
        db.session.commit()

        return u1, u2, u3


def test_get_leaderboard_orders():
    # Create only the 3 users above and nothing else.
    u1, _, _ = _setup_only_allowed_users()

    # get_leaderboard() uses Flask-SQLAlchemy's session, so it needs an app context.
    with app.app_context():
        # get_leaderboard() returns (weekly_score, username) pairs, sorted ascending.
        leaderboard = u1.get_leaderboard()

        # Sort rule: tuples are sorted by score first, then username for ties.
        assert leaderboard == [(5, "george"), (10, "james"), (10, "viraj")]