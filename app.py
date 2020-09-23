"""Import Flask, request,  and render_template."""
import os
from imghdr import what
from datetime import datetime
from flask import Flask, request, render_template, send_from_directory, \
    session
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

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.init_app(app)


###############################################################################
# DATABASE CLASSES
###############################################################################


class User(db.Model, UserMixin):
    """User database class."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_superadmin = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        """Return username and email for User."""
        return f"User('{self.username}', '{self.email}')"

    def __str__(self):
        """Return username and email for User."""
        return f"User('{self.username}', '{self.email}')"

    def set_superadmin(self):
        """Set Super Admin Privileges."""
        if self.email == "starlightromero@gmail.com":
            self.is_superadmin = True


class Product(db.Model):
    """Product database class."""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    img = db.Column(db.String(20), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        """Return title and price for Product."""
        return f"Product('{self.title}', '{self.price}')"

    def __str__(self):
        """Return title and price for Product."""
        return f"Product('{self.title}', '{self.price}')"


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


def add_product(title, price, file):
    """Add product to database."""
    file_path = save_file(file)
    if file_path:
        new_product = Product(title=title,
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
        title = request.form["title"]
        products = Product.query.filter(Product.title.contains(title))
        message = title
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
    return render_template("boards.html")


@app.route("/plywood")
def plywood():
    """Plywood page."""
    return "Plywood"


@app.route("/pressure-treated")
def pressure_treated():
    """Pressure treated page."""
    return "Pressure treated"


@app.route("/dimensional-lumber")
def dimensional_lumber():
    """Dimensional lumber page."""
    return "Dimensional lumber"


@app.route("/decking")
def decking():
    """Decking page."""
    return "Decking"


@app.route("/fencing")
def fencing():
    """Fencing page."""
    return "Fencing"


@app.route("/paneling")
def paneling():
    """Paneling page."""
    return "Paneling"


@app.route("/lattice")
def lattice():
    """Lattice page."""
    return "Lattice"


@app.route("/account", methods=['POST', 'GET'])
def profile():
    """Account page."""
    # if session['logged_in']:
    #     return render_template("account.html")
    # else:
    print(session)
    if request.method == 'GET':
        return render_template("log-in.html")
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password = sha256_crypt.hash(password)

        new_user = User(username=username,
                        email=email,
                        password=password)
        try:
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            session['logged_in'] = True
            message = "You have successfully logged in!"
        except(TypeError, ValueError):
            print("error")
        return render_template("account.html", message=message)


@app.route("/cart")
def cart():
    """Cart page."""
    return render_template("cart.html")


@app.route("/admin", methods=["POST", "GET"])
def admin():
    """Admin page."""
    if session['logged_in'] and request.method == "GET":
        products = Product.query.order_by(Product.date_created).all()
        return render_template("admin.html", products=products)
    if session['logged_in'] and request.method == "POST":
        try:
            button = request.form["button"]
            title = request.form["title"]
            if button == "Add Product":
                price = request.form["price"]
                uploaded_file = request.files['img']
                add_product(title, price, uploaded_file)
            elif button == "Delete Product":
                pass
        except(TypeError, ValueError):
            pass
        finally:
            products = Product.query.order_by(Product.date_created).all()
        return render_template("admin.html", products=products)
    return render_template("account.html")


@app.route('/admin/images/<filename>')
def upload(filename):
    """Upload image for new product."""
    return send_from_directory(app.config['UPLOAD_PATH'], filename)


@app.route("/admin/add-products")
def show_add_products():
    """Admin add products page."""
    return render_template("admin-add-products.html")


@app.route("/admin/delete-products")
def show_delete_products():
    """Admin delete projects page."""
    return render_template("admin-delete-products.html")


if __name__ == "__main__":
    app.run(debug=True)
