"""Import Flask, request,  and render_template."""
import os
from imghdr import what
from datetime import datetime
from flask import Flask, request,  render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png']
app.config['UPLOAD_PATH'] = 'static/product-images'

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    img = db.Column(db.String(20), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Product('{self.title}', '{self.price}')"


###############################################################################
# HELPER FUNCTIONS
###############################################################################


def validate_image(stream):
    """Validate a given image to jpg."""
    header = stream.read(512)
    stream.seek(0)
    format = what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')


###############################################################################
# ERROR HANDLING
###############################################################################

@app.errorhandler(404)
def page_not_found(e):
    print(e)
    return render_template("404.html")


@app.errorhandler(413)
def too_large(e):
    print(e)
    return "File is too large", 413

###############################################################################
# ROUTES
###############################################################################


@app.route("/")
def home():
    """Home page."""
    products = Product.query.order_by(Product.date_created).all()
    return render_template("home.html", products=products)


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


@app.route("/admin", methods=["POST", "GET"])
def admin():
    """Admin page."""
    if request.method == "GET":
        products = Product.query.order_by(Product.date_created).all()
        return render_template("admin.html", products=products)
    if request.method == "POST":
        try:
            button = request.form["button"]
            title = request.form["title"]
            if button == "Find Product":
                pass
            elif button == "Add Product":
                price = request.form["price"]
                uploaded_file = request.files['img']
                filename = secure_filename(uploaded_file.filename)
                if filename:
                    file_ext = os.path.splitext(filename)[1]
                    if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                            file_ext != validate_image(uploaded_file.stream):
                        return "Invalid image", 400
                    file_path = os.path.join(
                        app.config['UPLOAD_PATH'], filename
                    )
                    uploaded_file.save(file_path)
                    new_product = Product(title=title,
                                          price=price,
                                          img=file_path)
                    try:
                        db.session.add(new_product)
                        db.session.commit()
                    except(TypeError, ValueError):
                        pass
            elif button == "Delete Product":
                pass
            elif button == "Delete All Products":
                pass
        except(TypeError, ValueError):
            pass
        finally:
            products = Product.query.order_by(Product.date_created).all()
        return render_template("admin.html", products=products)


@app.route('/admin/products/images/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)


@app.route("/admin/find-products")
def show_find_products():
    """Admin find products page."""
    return render_template("admin-find-products.html")


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
