from datetime import datetime
from flask import current_app, url_for
from flask_login import UserMixin
from flask_mail import Message
from passlib.hash import sha256_crypt
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy.orm import backref
from online_store import db, login_manager, mail


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
    is_employee = db.Column(db.Boolean, nullable=False, default=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    categories = db.relationship("Category", backref="created_by", lazy=True)
    products = db.relationship("Product", backref="created_by", lazy=True)
    cart = db.relationship(
        "Cart", cascade="all, delete", backref="created_by", lazy=True
    )

    def __repr__(self):
        """Return username and email for User."""
        return f"BaseUser('{self.username}', '{self.email}')"

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

    def send_reset_email(self):
        """Send password reset email."""
        token = self.get_reset_token()
        msg = Message(
            "Password Reset Request",
            recipients=[self.email],
        )
        msg.body = f"""To reset your password, visit the following link:

    {url_for('users.reset_token', token=token, _external=True)}

    If you did not make this request, please ignore this email.
    """
        mail.send(msg)

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
        return self.link


class Product(db.Model):
    """Product database class."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(40), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    created_by_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    carts = db.relationship("Cart", secondary="product_cart_link")

    def __repr__(self):
        """Return name and price for Product."""
        return f"Product('{self.name}', '{self.category}','{self.price}')"

    def __str__(self):
        """Return name and price for Product."""
        return f"Product('{self.name}', '{self.category}', '{self.price}')"

    def set_quantity(self):
        """Decrement product quantity."""
        if self.quantity > 0:
            self.quantity -= 1
        return self.quantity


class ProductCartLink(db.Model):
    """ProductCartLink many-to-many database class."""

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    cart_id = db.Column(db.Integer, db.ForeignKey("cart.id"))
    product = db.relationship(
        "Product", backref=backref("link", cascade="all, delete-orphan")
    )
    cart = db.relationship(
        "Cart", backref=backref("link", cascade="all, delete-orphan")
    )


class Cart(db.Model):
    """Cart database class."""

    id = db.Column(db.Integer, primary_key=True)
    products = db.relationship("Product", secondary="product_cart_link")
    quantity = db.Column(db.Integer, default=0, nullable=False)
    subtotal = db.Column(db.Float, default=0, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        """Return quantity and subtotal for Cart."""
        return f"Cart('{self.quantity}', '${self.subtotal}', '{self.user_id}'"

    def __str__(self):
        """Return quantity and subtotal for Cart."""
        return (
            f"Cart('{self.quantity}', '${self.subtotal}', '{self.user_id}')"
        )

    def update_subtotal(self):
        """Update cart subtotal."""
        subtotal = 0
        for product in self.products:
            subtotal += product.price
        self.subtotal = subtotal
        return self.subtotal

    def add(self, product):
        """Add given product to cart."""
        self.products.append(product)
        self.quantity += 1
        product.set_quantity()
        self.update_subtotal()
        return self
