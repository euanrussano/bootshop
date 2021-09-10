from flask import render_template, request, redirect, url_for, session
from flask_login import current_user, login_required

from werkzeug.urls import url_parse
from datetime import datetime, timedelta

#from app import dummy_data

from app.shop.cart import CartManager
from app.catalog.models import Product, Category
from app.shop import bp

@bp.route('/')
@bp.route('/index')
@bp.route('/categoria/<category_slug>')
def index(category_slug=None):
    categories = Category.query.all()
    if category_slug:
        category = Category.query.filter_by(slug = category_slug).first()
        products = Product.query.filter_by(category_id = category.id).all()
    else:
        products = Product.query.all()

    cart = CartManager(session, current_user).get_cart()
    print('LENGTH = ', len(cart.items))
    return render_template('shop/index.html', title="Produtos", products=products, categories=categories,cart = cart)

@bp.route('/minha_conta')
@login_required
def user_account():
    if not current_user.is_authenticated():
        return redirect(url_for('auth.login'))
    return render_template('shop/profile.html', title="Minha Conta", current_user=current_user)
    

@bp.route('/produto/<product_slug>')
def product_detail(product_slug):
    product = Product.query.filter_by(slug = product_slug).first()
    return render_template('shop/product_detail.html', title=product.name, product = product, current_user=current_user)

@bp.route('/sacola')
def shopping_cart():
    cart = CartManager(session, current_user).get_cart()
    return render_template('shop/shopping_cart.html', title='Minha Sacola', current_user=current_user, cart=cart)