"""Import flask and models."""
from flask import Blueprint, render_template, request
from online_store.models import Category, Product

main = Blueprint("main", __name__)


@main.route("/home")
@main.route("/", methods=["GET", "POST"])
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


@main.route("/products/<product_id>", methods=["POST", "GET"])
def product_detail(product_id):
    """Product detail page."""
    categories = Category.query.all()
    product = Product.query.filter_by(id=product_id).first()
    context = {"categories": categories, "product": product}
    return render_template("product_details.html", **context)


@main.route("/category/<category_link>")
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


@main.route("/cart")
def cart():
    """Cart page."""
    categories = Category.query.all()
    context = {"categories": categories}
    return render_template("cart.html", **context)
