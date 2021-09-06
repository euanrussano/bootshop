from flask import render_template, request, redirect, url_for
from flask.helpers import flash
from flask_migrate import current
from flask_login import current_user, login_user, logout_user, login_required

from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User, Product, Category
from . import dummy_data

from werkzeug.urls import url_parse
from datetime import datetime, timedelta

@app.route('/')
@app.route('/index')
def index():
    return 'index'

@app.route('/painel')
def dashboard():

    #current_user = dummy_data.current_user
    
    messages = dummy_data.Message

    notifications = dummy_data.Notification
    
    today = datetime.today()
    first_day_curr_month = datetime(today.year, today.month, 1)
    if today.month > 1:
        first_day_prev_month = datetime(today.year, today.month-1, 1)
    else:
        first_day_prev_month = datetime(today.year-1, 12, 1)

    total_clients = User.query.filter_by(is_staff=False)
    current_month_clients = total_clients.filter(User.registered_at >= first_day_curr_month)
    prev_month_clients = total_clients.filter(User.registered_at < first_day_curr_month).filter(User.registered_at >= first_day_prev_month)
    if prev_month_clients.all():
        perc_month_inc_clients = ( len(current_month_clients.all()) - len(prev_month_clients.all()) )/len(prev_month_clients.all())*100
    else:
        perc_month_inc_clients = 100

    client_stats = { 'total': len(total_clients.all()) ,
                'new':  len(current_month_clients.all()),
                'perc_month': perc_month_inc_clients,
                'max': 'Not Implemented' }
    '''
    order_stats = {'total': dummy_data.get_orders_total(),
             'perc_month':dummy_data.get_orders_perc_month()}

    best_selling_products = dummy_data.get_best_selling_products()

    product_stats = {'total':len( dummy_data.Product.query.all() ),
                     'perc_month' : dummy_data.get_products_perc_month()}
    '''


    
    return render_template('dashboard.html', title='Painel', current_user=current_user,
                                                         messages=messages,
                                                         notifications=notifications,
                                                         client_stats = client_stats,
                                                         #order_stats = order_stats,
                                                         #best_selling_products = best_selling_products,
                                                         #product_stats = product_stats,
                                                         request = request
                                                         )

@app.route('/entrar', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is None or not user.check_password_hash(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc == '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title="Entrar", form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/cadastrar', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username = form.username.data,
                    email = form.email.data)
        user.set_password_hash(password = form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html',title="Cadastro", form=form)

    return render_template('register.html', title="Entrar")

@app.route('/recuperar-senha', methods=['GET', 'POST'])
def forgot_password():
    return render_template('forgot_password.html', title="Recuperar Senha")

@app.route('/minha_conta')
@login_required
def user_account():
    return render_template('profile.html', title="Minha Conta", current_user=current_user)

@app.route('/catalogo')
def products():
    products = Product.query.all()
    
    return render_template('products.html', title="Catálogo",  products = products,
                                                                current_user=current_user,
                                                                request = request)

@app.route('/categorias')
def categories():
    categories = Category.query.all()
    
    return render_template('categories.html', title="Catálogo",  categories = categories,
                                                                current_user=current_user,
                                                                request=request)