"""Import flask_wtf and wtforms."""
from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.validators import (
    DataRequired,
    NumberRange,
)
from wtforms.fields.html5 import IntegerField


class ChooseProductQuantity(FlaskForm):
    """Choose product quantity form."""

    quantity = IntegerField(
        "Quantity",
        validators=[DataRequired(), NumberRange(min=1, max=999)],
    )
