from flask import render_template, request, redirect, url_for
from flask.helpers import flash
from flask_migrate import current
from flask_login import current_user, login_user, logout_user, login_required

from app import app, db

from werkzeug.urls import url_parse
from datetime import datetime, timedelta

from app.auth import bp
from app.auth.models import User
from app.auth.forms import LoginForm, RegistrationForm


@bp.route('/entrar', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('shop.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is None or not user.check_password_hash(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc == '':
            next_page = url_for('shop.index')
        return redirect(next_page)
    return render_template('auth/login.html', title="Entrar", form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('shop.index'))

@bp.route('/cadastrar', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('shop.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username = form.username.data,
                    email = form.email.data)
        user.set_password_hash(password = form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html',title="Cadastro", form=form)

@bp.route('/recuperar-senha', methods=['GET', 'POST'])
def forgot_password():
    return render_template('auth/forgot_password.html', title="Recuperar Senha")

@bp.route('/minha_conta')
@login_required
def user_account():
    return render_template('auth/profile.html', title="Minha Conta", current_user=current_user)
