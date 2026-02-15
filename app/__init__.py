from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)   # ✅ remove custom static/template paths

app.config.from_object(Config)
db = SQLAlchemy(app)

from app import routes
