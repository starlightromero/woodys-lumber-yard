"""Import libraries and packages."""
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
    NumberRange,
)
from wtforms.fields.html5 import IntegerField, DecimalField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from online_store.models import Category


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
    price = DecimalField(
        "Price",
        default=0.00,
        places=2,
        validators=[DataRequired(), NumberRange(min=0)],
    )
    quantity = IntegerField(
        "In Stock",
        validators=[DataRequired(), NumberRange(min=1, max=999)],
    )
    image = FileField(
        "Add Product Image", validators=[FileAllowed(["jpg", "png"])]
    )
    submit = SubmitField("Add Product")


class UpdateProductForm(FlaskForm):
    """Update product form."""

    name = StringField(
        "Name", validators=[DataRequired(), Length(min=2, max=100)]
    )
    category = QuerySelectField(
        "Category",
        query_factory=lambda: Category.query,
        allow_blank=False,
        validators=[DataRequired()],
    )
    price = DecimalField(
        "Price", places=2, validators=[DataRequired(), NumberRange(min=0)]
    )
    quantity = IntegerField(
        "In Stock",
        validators=[DataRequired(), NumberRange(min=1, max=999)],
    )
    image = FileField(
        "Update Product Image", validators=[FileAllowed(["jpg", "png"])]
    )
    submit = SubmitField("Update Product")


class AddCategoryForm(FlaskForm):
    """Add category form."""

    name = StringField(
        "Name", validators=[DataRequired(), Length(min=2, max=20)]
    )
    submit = SubmitField("Add Category")


class UpdateCategoryForm(FlaskForm):
    """Update category form."""

    name = StringField(
        "Name", validators=[DataRequired(), Length(min=2, max=20)]
    )
