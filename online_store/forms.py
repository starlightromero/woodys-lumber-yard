from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    TextAreaField,
    DecimalField,
    SelectField,
)
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    EqualTo,
    ValidationError,
)
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from online_store.models import User, Category


class RegistrationForm(FlaskForm):
    """User resistration form."""

    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=8, max=20)]
    )
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        """Validate username is not taken."""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "That username is taken. Please choose a different username."
            )

    def validate_email(self, email):
        """Validate email is not in use."""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                """
                The email is already in use. Please enter a different email.
                Alternatively, if you forgot your password, go to the login
                page and click \"Forgot Password\".
                """
            )


class LoginForm(FlaskForm):
    """User login form."""

    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=8, max=20)]
    )
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class UpdateAccountForm(FlaskForm):
    """Update user account form."""

    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    image = FileField(
        "Update Profile Image", validators=[FileAllowed(["jpg", "png"])]
    )
    submit = SubmitField("Update")

    def validate_username(self, username):
        """Validate username is not taken."""
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    """That username is taken.
                    Please choose a different username.
                    """
                )

    def validate_email(self, email):
        """Validate email is not in use."""
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    """
                    The email is already in use. Please enter a different email.
                    Alternatively, if you forgot your password, go to the login
                    page and click \"Forgot Password\".
                    """
                )


class AddProductForm(FlaskForm):
    """Add product form."""

    name = StringField(
        "Name", validators=[DataRequired(), Length(min=2, max=100)]
    )
    category = QuerySelectField(
        "Category",
        query_factory=lambda: Category.query,
        allow_blank=False,
        validators=[DataRequired()],
    )
    price = DecimalField("Price", validators=[DataRequired()])
    image = FileField(
        "Add Product Image", validators=[FileAllowed(["jpg", "png"])]
    )
    submit = SubmitField("Add Product")


class AddCategoryForm(FlaskForm):
    """Add category form."""

    name = StringField(
        "Name", validators=[DataRequired(), Length(min=2, max=20)]
    )
    submit = SubmitField("Add Category")
