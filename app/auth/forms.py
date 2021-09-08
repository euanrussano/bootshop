from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField
from wtforms.fields.html5  import EmailField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Length

from app.auth.models import User


class LoginForm(FlaskForm):
    email = EmailField('Email', validators = [DataRequired(),])
    password = PasswordField('Senha', validators = [DataRequired(),])
    remember_me = BooleanField('Lembrar de mim')
    submit = SubmitField('Entrar')

class RegistrationForm(FlaskForm):
    username = StringField('Nome Completo', validators = [DataRequired(),])
    email = EmailField('Email', validators = [DataRequired(),])
    password = PasswordField('Senha', validators = [DataRequired(),])
    password2 = PasswordField('Repetir Senha', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Criar Cadastro')

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('Este e-mail já está sendo utilizado.')
