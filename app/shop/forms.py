from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField
from wtforms.fields.html5  import EmailField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Length

from app.auth.models import User


class AddToCartForm(FlaskForm):
    quantity = IntegerField('Quantidade', default=1)
    submit = SubmitField('Adicionar à sacola')