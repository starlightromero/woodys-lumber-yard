"""Import flask, login, and online_store."""
from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
)
from flask_login import login_required
from online_store import db
from online_store.models import Category, Product, User
from online_store.admin.forms import (
    AddCategoryForm,
    AddProductForm,
    UpdateProductForm,
    AddAdminForm,
)
from online_store.admin.utils import admin_required, super_admin_required
from online_store.main.utils import save_image

admin = Blueprint("admin", __name__)


@admin.route("/admin", methods=["POST", "GET"])
@login_required
@admin_required
def home():
    """Admin page."""
    categories = Category.query.all()
    products = Product.query.order_by(Product.date_created).all()
    context = {"products": products, "categories": categories}
    return render_template("admin/admin.html", **context)


@admin.route("/admin/category", methods=["GET", "POST"])
@login_required
@admin_required
def show_categories():
    """Admin add category page."""
    categories = Category.query.all()
    form = AddCategoryForm()
    if form.validate_on_submit():
        name = form.name.data.title()
        new_category = Category(name=name)
        new_category.add_link()
        db.session.add(new_category)
        db.session.commit()
        flash(f"{name} category has been added!")
        return redirect(url_for("admin.show_categories"))
    context = {
        "title": "Category",
        "form": form,
        "categories": categories,
    }
    return render_template("admin/category.html", **context)


@admin.route("/admin/category/<int:category_id>", methods=["DELETE"])
@login_required
@admin_required
def delete_category(category_id):
    """Admin delete category."""
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash(f"{category.name} category has been deleted.")
    return redirect(url_for("admin.show_categories"))


@admin.route("/admin/add_product", methods=["GET", "POST"])
@login_required
@admin_required
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
        return redirect(url_for("admin.show_categories"))
    context = {
        "title": "Add Product",
        "form": form,
        "categories": categories,
    }
    return render_template("admin/add_product.html", **context)


@admin.route("/admin/<int:product_id>/update", methods=["GET", "POST"])
@login_required
@admin_required
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
        return redirect(url_for("admin.home"))
    form.name.data = product.name
    form.category.data = product.category
    form.price.data = product.price
    context = {
        "title": "Update Product",
        "product": product,
        "categories": categories,
        "form": form,
    }
    return render_template("admin/update_product.html", **context)


@admin.route("/admin/<int:product_id>", methods=["DELETE"])
@login_required
@admin_required
def delete_product(product_id):
    """Admin delete product."""
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash(f"{product.name} product has been deleted.")
    return redirect(url_for("admin.home"))


@admin.route("/admin/add_admin", methods=["GET", "POST"])
@login_required
@super_admin_required
def add_admin():
    """Super admin add admin."""
    categories = Category.query.all()
    form = AddAdminForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.user.data)
        user.is_admin = True
        db.session.commit()
        flash(f"{user.name} has been granted admin permissions!")
        return redirect(url_for("admin.home"))
    context = {
        "title": "Add Admin",
        "form": form,
        "categories": categories,
    }
    return render_template("admin/add_admin.html", **context)
