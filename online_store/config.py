"""Import os and dotenv."""
import os
from dotenv import load_dotenv


class Config:
    """Config class."""

    ENV = "development"
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_USE_TTL = True
    MAIL_USE_SSL = True
    MAIL_DEBUG = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")
    MAIL_SUPPRESS_SEND = False
    MAIL_ASCII_ATTACHMENTS = False
