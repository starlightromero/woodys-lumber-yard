"""Import flask, login, online_store."""
from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
)
from flask_login import current_user, login_required, login_user, logout_user
from online_store import db
from online_store.models import Category, User
from online_store.users.forms import (
    LoginForm,
    RegistrationForm,
    UpdateAccountForm,
    RequestResetForm,
    ResetPasswordForm,
)
from online_store.main.utils import save_image
from online_store.users.utils import send_reset_email


users = Blueprint("users", __name__)


@users.route("/register", methods=["GET", "POST"])
def register():
    """Show register page."""
    if current_user.is_authenticated:
        redirect(url_for("main.home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = None
        if form.email.data == "starlightromero@gmail.com":
            user = User(
                username=form.username.data,
                email=form.email.data,
                is_admin=True,
                is_superadmin=True,
            )
        else:
            user = User(
                username=form.username.data,
                email=form.email.data,
            )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! You are now able to log in.")
        return redirect(url_for("users.login"))
    return render_template("register.html", title="Register", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    """Show login page."""
    if current_user.is_authenticated:
        redirect(url_for("main.home"))
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
                else redirect(url_for("main.home"))
            )
        flash("Login Unsuccessful. Please verify email and password.")
    context = {"title": "Login", "form": form, "categories": categories}
    return render_template("login.html", **context)


@users.route("/logout")
@login_required
def logout():
    """Logout current user and redirect to homepage."""
    logout_user()
    return redirect(url_for("main.home"))


@users.route("/account", methods=["GET", "POST"])
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
        return redirect(url_for("users.account"))
    form.username.data = current_user.username
    form.email.data = current_user.email
    context = {"title": "Account", "form": form, "categories": categories}
    return render_template("account.html", **context)


@users.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    """Show route for requesting user password reset."""
    if current_user.is_authenticated:
        redirect(url_for("main.home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent to reset your password.")
        return redirect(url_for("users.login"))
    context = {"title": "Reset Password", "form": form}
    return render_template("reset_request.html", **context)


@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    """Show route for resetting user password."""
    if current_user.is_authenticated:
        redirect(url_for("main.home"))
    user = User.verify_reset_token(token)
    if user is None:
        flash("The token is invalid or expired.")
        return redirect(url_for("users.reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash("Your password has been updated! You are now able to log in.")
        return redirect(url_for("users.login"))
    context = {"title": "Reset Password", "form": form}
    return render_template("reset_token.html", **context)
