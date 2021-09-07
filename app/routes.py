from flask import render_template, request, redirect, url_for
from flask_login import current_user

from werkzeug.urls import url_parse
from datetime import datetime, timedelta

from app import app, db
from app.forms import ProductForm
from app.models import Product, Category
from app import dummy_data

from app.auth.models import User

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



@app.route('/catalogo')
def product_list():
    products = Product.query.all()
    
    return render_template('product_list.html', title="Catálogo",  products = products,
                                                                current_user=current_user,
                                                                request = request)

@app.route("/catalogo/adicionar", methods=["GET", "POST"])
def product_add():
    product = Product()
    success = False

    if request.method == "POST":
        form = ProductForm(request.form, obj=product)
        if form.validate():
            form.populate_obj(product)
            db.session.add(product)
            db.session.commit()
            success = True
    else:
        form = ProductForm(obj=product)

    return render_template("product_add.html", form=form, success=success)


@app.route('/categorias')
def categories():
    categories = Category.query.all()
    
    return render_template('categories.html', title="Catálogo",  categories = categories,
                                                                current_user=current_user,
                                                                request=request)