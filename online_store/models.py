from datetime import datetime
from flask import current_app
from flask_login import UserMixin
from passlib.hash import sha256_crypt
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from online_store import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """User database class."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=True)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_superadmin = db.Column(db.Boolean, nullable=False, default=False)
    categories = db.relationship("Category", backref="created_by", lazy=True)
    products = db.relationship("Product", backref="created_by", lazy=True)

    def __repr__(self):
        """Return username and email for User."""
        return f"User('{self.username}', '{self.email}')"

    def __str__(self):
        """Return username and email for User."""
        return self.username

    def set_password(self, password):
        """Set user's password as hash."""
        self.password = sha256_crypt.hash(password)

    def check_password(self, password):
        """Check if given password matches hashed password."""
        return sha256_crypt.verify(password, self.password)

    def get_reset_token(self, expires_sec=900):
        """Generate user token to reset password."""
        s = Serializer(current_app.config["SECRET_KEY"], expires_sec)
        return s.dumps({"user_id": self.id}).decode("utf-8")

    @staticmethod
    def verify_reset_token(token):
        """Verify given token."""
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)["user_id"]
        except ValueError:
            return None
        return User.query.get(user_id)


class Category(db.Model):
    """Product Category database class."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    link = db.Column(db.String(20), nullable=True)
    products = db.relationship("Product", backref="category", lazy=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    created_by_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        """Return name for Category."""
        return f"Category('{self.name}', '{self.link}')"

    def __str__(self):
        """Return name for Category."""
        return self.name

    def add_link(self):
        """Add link based on category name."""
        self.link = self.name.lower().replace(" ", "-")


class Product(db.Model):
    """Product database class."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(40), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    created_by_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        """Return name and price for Product."""
        return f"Product('{self.name}', '{self.category}','{self.price}')"

    def __str__(self):
        """Return name and price for Product."""
        return f"Product('{self.name}', '{self.category}', '{self.price}')"
