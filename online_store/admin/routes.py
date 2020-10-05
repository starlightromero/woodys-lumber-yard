"""Import flask, login, and online_store."""
from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    jsonify,
)
from flask_login import login_required
from online_store import db
from online_store.models import Category, Product, User
from online_store.admin.forms import (
    AddCategoryForm,
    UpdateCategoryForm,
    AddProductForm,
    UpdateProductForm,
)
from online_store.admin.utils import admin_required, employee_required
from online_store.main.utils import save_image

admin = Blueprint("admin", __name__)


@admin.route("/admin", methods=["GET"])
@login_required
@employee_required
def home():
    """Admin page."""
    return redirect(url_for("admin.show_products"))


@admin.route("/admin/products", methods=["GET", "POST"])
@login_required
@employee_required
def show_products():
    """Admin add products page."""
    categories = Category.query.all()
    products = Product.query.order_by(Product.date_created).all()
    form = AddProductForm()
    if form.validate_on_submit():
        image_file = None
        if form.image.data:
            image_file = save_image(form.image.data, "product-images", 1000)
        name = form.name.data.title()
        new_product = Product(
            name=name,
            category=form.category.data,
            price=form.price.data,
            quantity=form.quantity.data,
            image=image_file,
        )
        db.session.add(new_product)
        db.session.commit()
        flash(f"{name} product has been added.")
        return redirect(url_for("admin.show_products"))
    context = {
        "title": "Products",
        "form": form,
        "categories": categories,
        "products": products,
    }
    return render_template("admin/products.html", **context)


@admin.route("/admin/<int:product_id>", methods=["GET", "POST"])
@login_required
@employee_required
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
        product.quantity = form.quantity.data
        db.session.commit()
        flash(f"{product.name} product has been updated.")
        return redirect(url_for("admin.show_products"))
    form.name.data = product.name
    form.category.data = product.category
    form.price.data = product.price
    form.quantity.data = product.quantity
    context = {
        "title": "Update Product",
        "product": product,
        "categories": categories,
        "form": form,
    }
    return render_template("admin/product_details.html", **context)


@admin.route("/admin/products/<int:product_id>", methods=["DELETE"])
@login_required
@employee_required
def delete_product(product_id):
    """Admin delete product."""
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash(f"{product.name} product has been deleted.")
    return redirect(url_for("admin.home"))


@admin.route("/admin/categories", methods=["GET", "POST"])
@login_required
@employee_required
def show_categories():
    """Admin add category page."""
    categories = Category.query.all()
    add_form = AddCategoryForm()
    update_form = UpdateCategoryForm()
    if add_form.validate_on_submit():
        name = add_form.name.data.title()
        new_category = Category(name=name)
        new_category.add_link()
        db.session.add(new_category)
        db.session.commit()
        flash(f"{name} category has been added.")
        return redirect(url_for("admin.show_categories"))
    context = {
        "title": "Categories",
        "add_form": add_form,
        "update_form": update_form,
        "categories": categories,
    }
    return render_template("admin/categories.html", **context)


@admin.route("/admin/categories/<int:category_id>", methods=["PUT"])
@login_required
@employee_required
def update_category(category_id):
    """Update delete category."""
    category = Category.query.get_or_404(category_id)
    name = request.json.get("name")
    category.name = name
    db.session.commit()
    flash(f"{category.name} has been updated.")
    return url_for("admin.show_categories")


@admin.route("/admin/categories/<int:category_id>", methods=["DELETE"])
@login_required
@employee_required
def delete_category(category_id):
    """Admin delete category."""
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash(f"{category.name} category has been deleted.")
    return url_for("admin.show_categories")


@admin.route("/admin/employees", methods=["GET"])
@login_required
@admin_required
def show_employees():
    """Admin add employee."""
    categories = Category.query.all()
    users = (
        User.query.filter_by(is_employee=False)
        .filter_by(is_admin=False)
        .all()
    )
    employees = User.query.filter_by(is_employee=True).all()
    context = {
        "title": "Admins",
        "categories": categories,
        "users": users,
        "employees": employees,
    }
    return render_template("admin/employees.html", **context)


@admin.route("/admin/employees/<int:user_id>", methods=["PUT"])
@login_required
@admin_required
def update_employees(user_id):
    """Update employee permissions."""
    user = User.query.get_or_404(user_id)
    if user.is_employee:
        user.is_employee = False
        flash(f"{user.username} had employee permissions revoked.")
    else:
        user.is_employee = True
        flash(f"{user.username} had employee permissions granted.")
    db.session.commit()
    return redirect(url_for("admin.show_employees"))
