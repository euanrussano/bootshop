from flask import render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import current_user, login_required

import os
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

from app import db, app
from app.utils import allowed_image

from app.auth.models import User
from app.auth.permissions import staff_only
from app.catalog.forms import ProductForm
from app.catalog.models import Category, Product, ProductImage
from app.logistics.forms import AddressForm
from app.logistics.models import Address

from app.dashboard import bp


@bp.route('/')
@login_required
@staff_only
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
@login_required
@staff_only
def product_list():
    products = Product.query.all()
    if 'message' in request.args:
        message = request.args['message']  # counterpart for url_for()
    
    return render_template('dashboard/product_list.html', title="Catálogo",  products = products,
                                                                current_user=current_user,
                                                                request = request,
                                                                message = message)

@bp.route("/produtos/editar/<product_slug>", methods=["GET", "POST"])
@staff_only
@login_required
def product_edit(product_slug):
    product = Product.query.filter_by(slug=product_slug)
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

@bp.route("/produtos/adicionar", methods=["GET", "POST"])
@staff_only
@login_required
def product_add():
    success = False

    if request.method == "POST":
        form = ProductForm(request.form)
        if form.validate():
            product = Product(name=form.name.data, description=form.description.data, category_id=form.category.data.id)
            message = ''

            uploaded_files = request.files.getlist("files[]")
            #uploaded_file = request.files("file")
            for uploaded_file in uploaded_files:
                print('FILENAME = ', uploaded_file.filename)
                if uploaded_file and allowed_image(uploaded_file.filename):
                    filename = secure_filename(uploaded_file.filename)
                    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    uploaded_file.save(image_path)
                    product_image = ProductImage(image_url = image_path, image_filename=image_path, product_id = product.id)
                    db.session.add(product_image)
                    message += f'Imagem {image_path} criado com sucesso.\n' 
                    
            db.session.add(product)
            db.session.commit()
            message += 'Produto criado com successo.'
            return redirect(url_for('dashboard.product_list', message = message))
    else:
        form = ProductForm()

    return render_template("dashboard/product_add.html", form=form, success=success)



@bp.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)


@bp.route('/categorias')
@login_required
@staff_only
def categories():
    categories = Category.query.all()
    
    return render_template('dashboard/categories.html', title="Catálogo",  categories = categories,
                                                                current_user=current_user,
                                                                request=request)


@bp.route('/enderecos')
@login_required
@staff_only
def address_list():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    addresses = Address.query.filter_by(user_id = current_user.id).all()
    return render_template('auth/address_list.html',title="Endereços", addresses=addresses)

@bp.route('/enderecos/<address_id>', methods=['GET', 'POST'])
@login_required
@staff_only
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
@login_required
@staff_only
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