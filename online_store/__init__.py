from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

app.config["ENV"] = "development"
app.config["DEBUG"] = True
app.config["TESTING"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024
app.config["UPLOAD_EXTENSIONS"] = [".jpg", ".png"]
app.config["UPLOAD_PATH"] = "static/product-images"
app.config["SECRET_KEY"] = "4721760cf3e19483f9fec4b7ead533d0"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.session_protection = "strong"
login_manager.login_view = "login"

from online_store import routes
