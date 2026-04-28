from app import app, db
from app.models import User
from flask_login import login_user


def setup_only_allowed_users():
    # Mark app as testing mode.
    app.config["TESTING"] = True  # this enables testing mode in Flask for us -

    # Bypass @login_required on /leaderboard so can test the leaderboard solely
    app.config["LOGIN_DISABLED"] = False

    app.config['WTF_CSRF_ENABLED'] = False
    app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False

    with app.app_context():
        # Ensure the DB contains ONLY the allowed users.
        db.drop_all()
        db.create_all()

        u1 = User(username="viraj", email="virajkc1@example.com")
        u1.set_password("hello")

        u2 = User(username="james", email="high@example.com")
        u2.set_password("hello")

        u3 = User(username="george", email="mid@example.com")
        u3.set_password("hello")

        db.session.add_all([u1, u2, u3])
        db.session.commit()


def setup_test(protein, carb, veg):
    setup_only_allowed_users()
    client = app.test_client()

    with app.test_request_context():
        with client:
            # login user
            test_user = User.query.first()
            login_user(test_user)

            # log meal
            log_meal = client.post("/log_meal", data={
                "protein_selected": protein,
                "carb_selected": carb,
                "veg_selected": veg
            }, follow_redirects=True)
            print(f"Final URL reached: {log_meal.request.url}")
            assert log_meal.status_code == 200

            db.session.refresh(test_user)

            return log_meal.get_data(as_text=True)


class TestCalculator:
    def test_highest_emission(self):
        # TESTING THE HIGHEST EMISSION MEAL POSSIBLE (beef, rice, tomato)
        response = setup_test("beef", "rice", "tomato")
        # test qualitative impact is correct
        assert "Very High" in response
        # test the correct image is shown
        assert "/static/images/very_high.png" in response
        # test kg of GHG is calculated correctly
        assert "9.488" in response
        # test equivalent miles is calculated correctly
        assert "23.7" in response

    def test_lowest_emission(self):
        # TESTING THE LOWEST EMISSION MEAL POSSIBLE (beans, bread, carrot)
        response = setup_test("beans", "bread", "carrot")
        # test qualitative impact is correct
        assert "Very Low" in response
        # test the correct image is shown
        assert "/static/images/very_low.png" in response
        # test kg of GHG is calculated correctly
        assert "0.154" in response
        # test equivalent miles is calculated correctly
        assert "0.4" in response
