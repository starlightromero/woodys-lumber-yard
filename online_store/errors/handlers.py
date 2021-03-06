"""Import flask and online_store."""
from flask import Blueprint, render_template
from online_store.models import Category

errors = Blueprint("errors", __name__)


@errors.app_errorhandler(404)
def page_not_found(error):
    """Page not found page."""
    print(error)
    categories = Category.query.all()
    context = {"categories": categories}
    return render_template("errors/404.html", **context), 404


@errors.app_errorhandler(500)
def internal_error(error):
    """Internal error page."""
    print(error)
    categories = Category.query.all()
    context = {"categories": categories}
    return render_template("errors/500.html", **context), 500
