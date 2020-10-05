"""Import flask and models."""
from flask import Blueprint, render_template, request, url_for
from flask_login import current_user
from online_store import db
from online_store.models import Category, Product, Cart

main = Blueprint("main", __name__)


@main.route("/home")
@main.route("/", methods=["GET", "POST"])
def home():
    """Home page."""
    categories = Category.query.all()
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if request.method == "POST":
        name = request.form["name"]
        products = Product.query.filter(Product.name.contains(name))
        search_message = name
        context = {
            "categories": categories,
            "search_message": search_message,
            "products": products,
            "cart": cart,
        }
    else:
        products = Product.query.order_by(Product.date_created).all()
        context = {
            "categories": categories,
            "products": products,
            "cart": cart,
        }
    # try:
    #     if current_user.is_employee:
    #         return render_template("admin/admin.html", **context)
    # except AttributeError:
    #     pass
    return render_template("home.html", **context)


@main.route("/products/<product_id>", methods=["POST", "GET"])
def product_detail(product_id):
    """Product detail page."""
    categories = Category.query.all()
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    product = Product.query.filter_by(id=product_id).first()
    context = {"categories": categories, "product": product, "cart": cart}
    return render_template("product_details.html", **context)


@main.route("/category/<category_link>")
def product_category(category_link):
    """Category page."""
    categories = Category.query.all()
    category = Category.query.filter_by(link=category_link).first()
    cart = Cart.query.filter_by(user_id=current_user.id).first()
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
        "cart": cart,
    }
    return render_template("home.html", **context)


@main.route("/cart", methods=["GET"])
def show_cart():
    """Cart page."""
    categories = Category.query.all()
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    context = {"categories": categories, "cart": cart}
    return render_template("cart.html", **context)


@main.route("/cart/<int:product_id>", methods=["PUT"])
def add_to_cart(product_id):
    """Add product to cart."""
    product = Product.query.get_or_404(product_id)
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if cart is None:
        cart = Cart(user_id=current_user.id)
        db.session.add(cart)
        db.session.commit()
    cart.add(product)
    db.session.commit()
    return url_for("main.show_cart")
