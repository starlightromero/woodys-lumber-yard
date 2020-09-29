import os
import secrets
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
from online_store.forms import (
    RegistrationForm,
    LoginForm,
    UpdateAccountForm,
    AddProductForm,
    UpdateProductForm,
    CategoryForm,
)

###############################################################################
#                           HELPER FUNCTIONS
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


###############################################################################
#                           ERROR HANDLING
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
#                           `   ROUTES
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


@app.route("/category/<category_link>")
def product_category(category_link):
    """Category page."""
    categories = Category.query.all()
    category = Category.query.filter_by(link=category_link).first()
    title = category.name
    products = (
        Product.query.filter_by(category_id=category.id)
        .order_by(Product.date_created)
        .all()
    )
    context = {
        "products": products,
        "title": title,
        "categories": categories,
    }
    return render_template("home.html", **context)


###############################################################################
#                               ACCOUNT ROUTES
###############################################################################


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
    categories = Category.query.all()
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
    context = {"title": "Login", "form": form, "categories": categories}
    return render_template("login.html", **context)


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
    form.username.data = current_user.username
    form.email.data = current_user.email
    context = {"title": "Account", "form": form, "categories": categories}
    return render_template("account.html", **context)


@app.route("/cart")
def cart():
    """Cart page."""
    categories = Category.query.all()
    context = {"categories": categories}
    return render_template("cart.html", **context)


###############################################################################
#                               ADMIN ROUTES
###############################################################################


@app.route("/admin", methods=["POST", "GET"])
@login_required
def admin():
    """Admin page."""
    categories = Category.query.all()
    products = Product.query.order_by(Product.date_created).all()
    context = {"products": products, "categories": categories}
    return render_template("admin.html", **context)


@app.route("/admin/add-category", methods=["GET", "POST"])
@login_required
def add_category():
    """Admin add category page."""
    categories = Category.query.all()
    form = CategoryForm()
    if form.validate_on_submit():
        name = form.name.data.title()
        new_category = Category(name=name)
        new_category.add_link()
        db.session.add(new_category)
        db.session.commit()
        flash(f"{name} category has been added!")
        return redirect(url_for("add_category"))
    context = {
        "title": "Add Category",
        "form": form,
        "categories": categories,
    }
    return render_template("admin-add-category.html", **context)


@app.route("/admin/<int:category_id>/delete", methods=["POST"])
@login_required
def delete_category(category_id):
    """Admin delete category."""
    return redirect(url_for("admin"))


@app.route("/admin/add-product", methods=["GET", "POST"])
@login_required
def add_product():
    """Admin add products page."""
    categories = Category.query.all()
    form = AddProductForm()
    if form.validate_on_submit():
        image_file = None
        if form.image.data:
            image_file = save_image(form.image.data, "product-images", 800)
        name = form.name.data.title()
        new_product = Product(
            name=name,
            category=form.category.data,
            price=form.price.data,
            image=image_file,
        )
        db.session.add(new_product)
        db.session.commit()
        flash(f"{name} product has been added!")
        return redirect(url_for("add_category"))
    context = {
        "title": "Add Product",
        "form": form,
        "categories": categories,
    }
    return render_template("admin-add-product.html", **context)


@app.route("/admin/<int:product_id>/update", methods=["GET", "POST"])
@login_required
def update_product(product_id):
    """Admin update product."""
    categories = Category.query.all()
    product = Product.query.get_or_404(product_id)
    form = UpdateProductForm()
    if form.validate_on_submit():
        if form.image.data:
            product.image = save_image(form.image.data, "product-images", 800)
        product.name = form.name.data.title()
        product.category = form.category.data
        product.price = form.price.data
        db.session.commit()
        flash(f"{product.name} product has been updated.")
        return redirect(url_for("admin"))
    form.name.data = product.name
    form.category.data = product.category
    form.price.data = product.price
    context = {
        "title": "Update Product",
        "product": product,
        "categories": categories,
        "form": form,
    }
    return render_template("admin-update-product.html", **context)


@app.route("/admin/<int:product_id>/delete", methods=["POST"])
@login_required
def delete_product(product_id):
    """Admin delete product."""
    product = Product.query.get_or_404(product_id)
    print(product)
    db.session.delete(product)
    db.session.commit()
    flash(f"{product.name} product has been deleted.")
    return redirect(url_for("admin"))
