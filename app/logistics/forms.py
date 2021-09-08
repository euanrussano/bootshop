from flask_wtf import FlaskForm
from wtforms.fields.simple import TextAreaField

from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.fields.html5  import EmailField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Length

from wtforms_sqlalchemy.fields import QuerySelectField

from app.catalog.models import Category

class AddressForm(FlaskForm):
    address = StringField('Endereço (Rua Número, Bairro)', validators=[DataRequired()])
    postal_code = IntegerField('CEP', validators = [DataRequired(), Length(min=8, max=8)])
    city = StringField('Cidade', validators=[DataRequired()])
    state = StringField('Estado', validators=[DataRequired(), Length(min=2, max=2)])
    submit = SubmitField('Editar/Adicionar Endereço')
