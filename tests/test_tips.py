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


def _test_template(protein, response_message):
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
                "carb_selected": "pasta",
                "veg_selected": "tomato"
            }, follow_redirects=True)
            assert log_meal.status_code == 200

            db.session.refresh(test_user)

            # check response message is the same as we predict
            response = client.get("/")
            body = response.get_data(as_text=True)
            assert response_message in body


class TestTips:
    def test_beef(self):
        _test_template("beef", "Try swapping out beef for pork!")

    def test_shrimp(self):
        _test_template("shrimp", "Try swapping out shrimp for wild fish!")

    def test_low_impact(self):
        _test_template("beans", "You have a very low environmental impact, keep doing what you're doing!")

    def test_tip_aging(self):
        setup_only_allowed_users()
        client = app.test_client()

        with app.test_request_context():
            with client:
                test_user = User.query.first()
                login_user(test_user)

                # log a beef meal and check response
                log_meal = client.post("/log_meal", data={
                    "protein_selected": "beef",
                    "carb_selected": "pasta",
                    "veg_selected": "tomato"
                }, follow_redirects=True)
                assert log_meal.status_code == 200
                db.session.refresh(test_user)
                response = client.get("/")
                body = response.get_data(as_text=True)
                assert "Try swapping out beef for pork!" in body

                # log 6 low-emission meals and check the same response is given as before
                for i in range(6):
                    log_meal = client.post("/log_meal", data={
                        "protein_selected": "beans",
                        "carb_selected": "pasta",
                        "veg_selected": "tomato"
                    }, follow_redirects=True)
                    assert log_meal.status_code == 200
                    db.session.refresh(test_user)
                    response = client.get("/")
                    body = response.get_data(as_text=True)
                    assert "Try swapping out beef for pork!" in body

                # log a 7th low-emission meal and test that the response changes
                log_meal = client.post("/log_meal", data={
                    "protein_selected": "beans",
                    "carb_selected": "pasta",
                    "veg_selected": "tomato"
                }, follow_redirects=True)
                assert log_meal.status_code == 200
                db.session.refresh(test_user)
                response = client.get("/")
                body = response.get_data(as_text=True)
                assert "You have a very low environmental impact, keep doing what you're doing!" in body
