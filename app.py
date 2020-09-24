"""Import Flask, request,  and render_template."""
import os
from imghdr import what
from datetime import datetime
from flask import Flask, request, render_template, send_from_directory, \
    session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, current_user, login_user, \
    logout_user
from passlib.hash import sha256_crypt
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png']
app.config['UPLOAD_PATH'] = 'static/product-images'
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.init_app(app)


###############################################################################
# DATABASE CLASSES
###############################################################################


class User(db.Model, UserMixin):
    """User database class."""

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_superadmin = db.Column(db.Boolean, nullable=False, default=False)
    categories = db.relationship('Category', backref='created_by', lazy=True)
    products = db.relationship('Product', backref='created_by', lazy=True)

    def __repr__(self):
        """Return username and email for User."""
        return f"User('{self.username}', '{self.email}')"

    def __str__(self):
        """Return username and email for User."""
        return f"User('{self.username}', '{self.email}')"


class Category(db.Model):
    """Product Category database class."""

    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    products = db.relationship('Product', backref='category', lazy=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        """Return name for Category."""
        return f"Product('{self.name}')"

    def __str__(self):
        """Return name for Category."""
        return f"Product('{self.name}')"


class Product(db.Model):
    """Product database class."""

    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    price = db.Column(db.Float, nullable=False)
    img = db.Column(db.String(40), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        """Return name and price for Product."""
        return f"Product('{self.name}', '{self.price}')"

    def __str__(self):
        """Return name and price for Product."""
        return f"Product('{self.name}', '{self.price}')"


###############################################################################
# HELPER FUNCTIONS
###############################################################################


@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()


def validate_image(stream):
    """Validate a given image to jpg."""
    print("IN VALIDATE")
    header = stream.read(512)
    stream.seek(0)
    img_format = what(None, header)
    print(img_format)
    if not img_format:
        return None
    return '.' + (img_format if img_format != 'jpeg' else 'jpg')


def save_file(file):
    """Check security on file and save to upload path."""
    filename = secure_filename(file.filename)
    if filename:
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                file_ext != validate_image(file.stream):
            return "Invalid image", 400
        file_path = os.path.join(
            app.config['UPLOAD_PATH'], filename
        )
        file.save(file_path)
        return file_path


def add_product(name, price, file):
    """Add product to database."""
    file_path = save_file(file)
    if file_path:
        new_product = Product(name=name,
                              price=price,
                              img=file_path)
        try:
            db.session.add(new_product)
            db.session.commit()
        except(TypeError, ValueError):
            print("error")


###############################################################################
# ERROR HANDLING
###############################################################################


@app.errorhandler(404)
def page_not_found(e):
    """Page not found page."""
    print(e)
    return render_template("404.html")


@app.errorhandler(413)
def too_large(e):
    """File is too large page."""
    print(e)
    return "File is too large", 413

###############################################################################
# ROUTES
###############################################################################


@app.route("/", methods=["GET", "POST"])
def home():
    """Home page."""
    if request.method == "POST":
        name = request.form["name"]
        products = Product.query.filter(Product.name.contains(name))
        message = name
        context = {
            'products': products,
            'message': message
        }
    else:
        products = Product.query.order_by(Product.date_created).all()
        context = {
            'products': products,
        }
    return render_template("home.html", **context)


@app.route("/products/<product_id>", methods=['POST', 'GET'])
def product_detail(product_id):
    """Product detail page."""
    product = Product.query.filter_by(id=product_id).first()
    return render_template("product-details.html", product=product)


@app.route("/boards")
def boards():
    """Boards page."""
    products = Product.query.order_by(Product.date_created).all()
    context = {
        'products': products,
        'title': 'Boards'
    }
    return render_template("home.html", **context)


@app.route("/plywood")
def plywood():
    """Plywood page."""
    products = Product.query.order_by(Product.date_created).all()
    context = {
        'products': products,
        'title': 'Plywood'
    }
    return render_template("home.html", **context)


@app.route("/pressure-treated")
def pressure_treated():
    """Pressure treated page."""
    products = Product.query.order_by(Product.date_created).all()
    context = {
        'products': products,
        'title': 'Pressure Treated'
    }
    return render_template("home.html", **context)


@app.route("/dimensional-lumber")
def dimensional_lumber():
    """Dimensional lumber page."""
    products = Product.query.order_by(Product.date_created).all()
    context = {
        'products': products,
        'title': 'Dimensional Lumber'
    }
    return render_template("home.html", **context)


@app.route("/decking")
def decking():
    """Decking page."""
    products = Product.query.order_by(Product.date_created).all()
    context = {
        'products': products,
        'title': 'Decking'
    }
    return render_template("home.html", **context)


@app.route("/fencing")
def fencing():
    """Fencing page."""
    products = Product.query.order_by(Product.date_created).all()
    context = {
        'products': products,
        'title': 'Fencing'
    }
    return render_template("home.html", **context)


@app.route("/paneling")
def paneling():
    """Paneling page."""
    products = Product.query.order_by(Product.date_created).all()
    context = {
        'products': products,
        'title': 'Paneling'
    }
    return render_template("home.html", **context)


@app.route("/lattice")
def lattice():
    """Lattice page."""
    products = Product.query.order_by(Product.date_created).all()
    context = {
        'products': products,
        'title': 'Lattice'
    }
    return render_template("home.html", **context)


@app.route("/account", methods=['POST', 'GET'])
def account():
    """Account page."""
    try:
        if session['logged_in']:
            return render_template("account.html")
    except KeyError:
        if request.method == 'GET':
            return render_template("log-in.html")
        if request.method == 'POST':
            button = request.form['submit']
            message = "There was an error with accessing your account."
            if button == 'Sign Up':
                username = request.form['username']
                email = request.form['email']
                password = request.form['password']
                password = sha256_crypt.hash(password)
                is_admin = False
                is_superadmin = False
                if email == "starlightromero@gmail.com":
                    is_superadmin = True
                    is_admin = True

                new_user = User(username=username,
                                email=email,
                                password=password,
                                is_admin=is_admin,
                                is_superadmin=is_superadmin)
                try:
                    db.session.add(new_user)
                    db.session.commit()
                    login_user(new_user)
                    session['logged_in'] = True
                    message = "You have successfully signed up!"
                except(TypeError, ValueError):
                    print("error")
            elif button == 'Log In':
                message = 'You have successfully logged in!'
            return render_template("account.html", message=message)


@app.route("/cart")
def cart():
    """Cart page."""
    return render_template("cart.html")


@app.route("/admin", methods=["POST", "GET"])
def admin():
    """Admin page."""
    try:
        if session['logged_in'] and request.method == "GET":
            products = Product.query.order_by(Product.date_created).all()
            return render_template("admin.html", products=products)
        if session['logged_in'] and request.method == "POST":
            try:
                button = request.form["button"]
                name = request.form["name"]
                if button == "Add Product":
                    price = request.form["price"]
                    uploaded_file = request.files['img']
                    add_product(name, price, uploaded_file)
                elif button == "Delete Product":
                    pass
                elif button == "Add Category":
                    new_category = Category(name=name)
                    try:
                        db.session.add(new_category)
                        db.session.commit()
                    except(TypeError, ValueError):
                        print("error")
                elif button == "Delete Category":
                    pass
            except(TypeError, ValueError):
                pass
            finally:
                products = Product.query.order_by(Product.date_created).all()
            return render_template("admin.html", products=products)
    except KeyError:
        return redirect(url_for('account'))


@app.route('/admin/images/<filename>')
def upload(filename):
    """Upload image for new product."""
    return send_from_directory(app.config['UPLOAD_PATH'], filename)


@app.route("/admin/add-category")
def show_add_category():
    """Admin add category page."""
    return render_template("admin-add-category.html")


@app.route("/admin/delete-category")
def show_delete_category():
    """Admin delete category page."""
    return render_template("admin-delete-category.html")


@app.route("/admin/add-products")
def show_add_products():
    """Admin add products page."""
    categories = Category.query.order_by(Category.name).all()
    return render_template("admin-add-products.html", categories=categories)


@app.route("/admin/delete-products")
def show_delete_products():
    """Admin delete projects page."""
    return render_template("admin-delete-products.html")


if __name__ == "__main__":
    app.run(debug=True)
