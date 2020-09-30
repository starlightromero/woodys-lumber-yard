"""Import login, wtf, and wtforms."""
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
)
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    EqualTo,
    ValidationError,
)
from online_store.models import User


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


class RequestResetForm(FlaskForm):
    """Request password reset form."""

    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")

    def validate_email(self, email):
        """Validate email is associated with a user."""
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(
                """
                There is no account associated with that email.
                Please sign up for an account.
                """
            )


class ResetPasswordForm(FlaskForm):
    """Reset password form."""

    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=8, max=20)]
    )
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Reset Password")
