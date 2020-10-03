from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from online_store.config import Config

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
login_manager.session_protection = "strong"
login_manager.login_view = "users.login"


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    from online_store.main.routes import main
    from online_store.users.routes import users
    from online_store.admin.routes import admin
    from online_store.errors.handlers import errors

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(admin)
    app.register_blueprint(errors)

    with app.app_context():
        db.create_all()

    return app
