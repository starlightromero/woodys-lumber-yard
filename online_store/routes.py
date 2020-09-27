import os
import secrets
from werkzeug.utils import secure_filename
from PIL import Image
from flask import (
    render_template,
    flash,
    redirect,
    url_for,
    request,
    abort,
    send_from_directory,
)
from flask_login import login_user, current_user, logout_user, login_required
from online_store import app, db
from online_store.models import User, Category, Product
from online_store.forms import RegistrationForm, LoginForm, UpdateAccountForm

###############################################################################
# HELPER FUNCTIONS
###############################################################################


def save_image(form_image, folder, size):
    """Save image to profile_images."""
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_image.filename)
    image_filename = random_hex + f_ext
    image_path = os.path.join(
        app.root_path, f"static/{folder}", image_filename
    )
    output_size = (size, size)
    i = Image.open(form_image)
    i.thumbnail(output_size)
    i.save(image_path)
    return image_filename


def validate_image(stream):
    """Validate a given image to jpg."""
    header = stream.read(512)
    stream.seek(0)
    img_format = what(None, header)
    if not img_format:
        return None
    return "." + (img_format if img_format != "jpeg" else "jpg")


def save_file(file):
    """Check security on file and save to upload path."""
    filename = secure_filename(file.filename)
    if filename:
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config[
            "UPLOAD_EXTENSIONS"
        ] or file_ext != validate_image(file.stream):
            return "Invalid image", 400
        file_path = os.path.join(app.config["UPLOAD_PATH"], filename)
        file.save(file_path)
        return file_path


def add_product(name, category, price, file):
    """Add product to database."""
    file_path = save_file(file)
    if file_path:
        new_product = Product(
            name=name, category=category, price=price, img=file_path
        )
        try:
            db.session.add(new_product)
            db.session.commit()
        except (TypeError, ValueError):
            print("error")


###############################################################################
# ERROR HANDLING
###############################################################################


@app.errorhandler(404)
def page_not_found(e):
    """Page not found page."""
    print(e)
    categories = Category.query.all()
    context = {"categories": categories}
    return render_template("404.html", **context), 404


@app.errorhandler(413)
def too_large(e):
    """File is too large page."""
    print(e)
    return "File is too large", 413


###############################################################################
# ROUTES
###############################################################################


@app.route("/home")
@app.route("/", methods=["GET", "POST"])
def home():
    """Home page."""
    categories = Category.query.all()
    if request.method == "POST":
        name = request.form["name"]
        products = Product.query.filter(Product.name.contains(name))
        search_message = name
        context = {
            "categories": categories,
            "search_message": search_message,
            "products": products,
        }
    else:
        products = Product.query.order_by(Product.date_created).all()
        context = {"categories": categories, "products": products}
    return render_template("home.html", **context)


@app.route("/products/<product_id>", methods=["POST", "GET"])
def product_detail(product_id):
    """Product detail page."""
    categories = Category.query.all()
    product = Product.query.filter_by(id=product_id).first()
    context = {"categories": categories, "product": product}
    return render_template("product-details.html", **context)


@app.route("/category/<category>")
def boards(category):
    """Category page."""
    categories = Category.query.all()
    title = category.replace("-", " ").title()
    try:
        products = (
            Product.query.filter_by(link=category)
            .order_by(Product.date_created)
            .all()
        )
        context = {
            "products": products,
            "title": title,
            "categories": categories,
        }
        return render_template("home.html", **context)
    except:
        message = "No products found."
        context = {
            "title": title,
            "categories": categories,
            "message": message,
        }
        return render_template("home.html", **context)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Show register page."""
    if current_user.is_authenticated:
        redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! You are now able to log in.")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Show login page."""
    if current_user.is_authenticated:
        redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return (
                redirect(next_page)
                if next_page
                else redirect(url_for("home"))
            )
        flash("Login Unsuccessful. Please verify email and password.")
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
@login_required
def logout():
    """Logout current user and redirect to homepage."""
    logout_user()
    return redirect(url_for("home"))


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    """Account page."""
    categories = Category.query.all()
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.image.data:
            image_file = save_image(form.image.data, "profile-images", 125)
            current_user.image = image_file
        current_user.username = form.username.data
        current_user.email = form.username.data
        db.session.commit()
        flash("Your account has been updated!")
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template("account.html", title="Account", form=form)


@app.route("/cart")
def cart():
    """Cart page."""
    categories = Category.query.all()
    context = {"categories": categories}
    return render_template("cart.html", **context)


###############################################################################
# ADMIN ROUTES
###############################################################################


@app.route("/admin", methods=["POST", "GET"])
@login_required
def admin():
    """Admin page."""
    categories = Category.query.all()
    try:
        if session["logged_in"] and request.method == "GET":
            products = Product.query.order_by(Product.date_created).all()
            context = {"products": products, "categories": categories}
            return render_template("admin.html", **context)
        if session["logged_in"] and request.method == "POST":
            try:
                button = request.form["button"]
                name = request.form["name"]
                if button == "Add Product":
                    category_id = request.form["category"]
                    category = Category.query.filter_by(
                        id=category_id
                    ).first()
                    price = request.form["price"]
                    uploaded_file = request.files["img"]
                    add_product(name, category, price, uploaded_file)
                    message = f"{name} has been successfully added."
                elif button == "Delete Product":
                    pass
                elif button == "Add Category":
                    name = name.title()
                    link = name.lower().replace(" ", "-")
                    new_category = Category(name=name, link=link)
                    try:
                        db.session.add(new_category)
                        db.session.commit()
                        message = f"{name} has been successfully added."
                    except (TypeError, ValueError):
                        print("error")
                elif button == "Delete Category":
                    pass
            except (TypeError, ValueError):
                message = "In the except"
            finally:
                products = Product.query.order_by(Product.date_created).all()
                context = {
                    "categories": categories,
                    "products": products,
                    "message": message,
                }
            return render_template("admin.html", **context)
    except KeyError:
        return redirect(url_for("account"))


@app.route("/admin/images/<filename>")
@login_required
def upload(filename):
    """Upload image for new product."""
    return send_from_directory(app.config["UPLOAD_PATH"], filename)


@app.route("/admin/add-category")
@login_required
def show_add_category():
    """Admin add category page."""
    categories = Category.query.all()
    context = {"categories": categories}
    return render_template("admin-add-category.html", **context)


@app.route("/admin/delete-category")
@login_required
def show_delete_category():
    """Admin delete category page."""
    categories = Category.query.all()
    context = {"categories": categories}
    return render_template("admin-delete-category.html", **context)


@app.route("/admin/add-product")
@login_required
def show_add_product():
    """Admin add products page."""
    categories = Category.query.order_by(Category.name).all()
    return render_template("admin-add-product.html", categories=categories)


@app.route("/admin/delete-product")
@login_required
def show_delete_product():
    """Admin delete projects page."""
    categories = Category.query.all()
    context = {"categories": categories}
    return render_template("admin-delete-productshtml", **context)
