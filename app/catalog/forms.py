from flask_wtf import FlaskForm
from wtforms.fields.simple import TextAreaField

from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.html5  import EmailField
from wtforms.validators import DataRequired, EqualTo, ValidationError

from wtforms_sqlalchemy.fields import QuerySelectField

from app.catalog.models import Category


def enabled_categories():
    return Category.query.all()

class ProductForm(FlaskForm):
    name = StringField('Nome', validators = [DataRequired(),])
    description = TextAreaField('Descrição', validators = [DataRequired(),])
    category = QuerySelectField(query_factory=enabled_categories, get_label="name", allow_blank=False)
    submit = SubmitField('Criar Produto')

class CategoryForm(FlaskForm):
    name = StringField('Nome', validators = [DataRequired(),])
    submit = SubmitField('Criar Categoria')