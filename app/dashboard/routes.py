
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user

from werkzeug.urls import url_parse
from datetime import datetime, timedelta

from app import db

from app.auth.models import User
from app.catalog.forms import ProductForm
from app.catalog.models import Category, Product
from app.logistics.forms import AddressForm
from app.logistics.models import Address

from app.dashboard import bp


@bp.route('/')
def index():

    #current_user = dummy_data.current_user
    
    #messages = dummy_data.Message

    #notifications = dummy_data.Notification
    
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


    
    return render_template('dashboard/index.html', title='Painel', current_user=current_user,
                                                         #messages=messages,
                                                         #notifications=notifications,
                                                         client_stats = client_stats,
                                                         #order_stats = order_stats,
                                                         #best_selling_products = best_selling_products,
                                                         #product_stats = product_stats,
                                                         request = request
                                                         )



@bp.route('/produtos')
def product_list():
    products = Product.query.all()
    
    return render_template('dashboard/product_list.html', title="Catálogo",  products = products,
                                                                current_user=current_user,
                                                                request = request)

@bp.route("/produtos/adicionar", methods=["GET", "POST"])
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

    return render_template("dashboard/product_add.html", form=form, success=success)


@bp.route('/categorias')
def categories():
    categories = Category.query.all()
    
    return render_template('dashboard/categories.html', title="Catálogo",  categories = categories,
                                                                current_user=current_user,
                                                                request=request)


@bp.route('/enderecos')
def address_list():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    addresses = Address.query.filter_by(user_id = current_user.id).all()
    return render_template('auth/address_list.html',title="Endereços", addresses=addresses)

@bp.route('/enderecos/<address_id>', methods=['GET', 'POST'])
def address_detail(address_id):
    address = Address.query.get(address_id)
    if not current_user.is_authenticated or not address.user_id == current_user.id:
        return redirect(url_for('index'))
    form = AddressForm(obj=address)
    if form.validate_on_submit():
        form.populate_obj(address)
        db.session.commit()
        flash('As mudanças no endereço foram salvas')
        return redirect(url_for('address_list'))
    return render_template('address_add.html', title='Editar Endereço',form=form)

@bp.route('/enderecos/novo', methods=['GET', 'POST'])
def address_add():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    form = AddressForm()
    if form.validate_on_submit():
        address = Address()
        form.populate_obj(address)
        db.session.add(address)
        db.session.commit()
        flash('O novo endereço foi salvo')
        return redirect(url_for('address_list'))
    return render_template('address_add.html', title='Adicionar Endereço',form=form)