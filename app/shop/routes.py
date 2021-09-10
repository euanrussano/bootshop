from flask import render_template, request, redirect, url_for, session
from flask_login import current_user, login_required

from werkzeug.urls import url_parse
from datetime import datetime, timedelta

#from app import dummy_data

from app.shop.cart import CartManager
from app.catalog.models import Product, Category, ProductStock
from app.shop import bp
from app.shop.forms import AddToCartForm

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
    
    return render_template('shop/index.html', title="Produtos", products=products, categories=categories,cart = cart)

@bp.route('/minha_conta')
@login_required
def user_account():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    cart = CartManager(session, current_user).get_cart()
    return render_template('shop/profile.html', title="Minha Conta", current_user=current_user, cart=cart)
    

@bp.route('/produto/<product_slug>', methods=['GET', 'POST'])
def product_detail(product_slug):
    product = Product.query.filter_by(slug = product_slug).first()
    cart = CartManager(session, current_user).get_cart()
    addToCartForm = AddToCartForm()
    if addToCartForm.validate_on_submit():
        product_stock = ProductStock.query.filter_by(product_id = product.id).first()
        cart_manager = CartManager(session, current_user)
        print('SESSION CART ID = ',session['CART_ID'])
        cart_manager.add(product_stock, addToCartForm.quantity.data)
        return redirect(url_for('shop.shopping_cart'))
    return render_template('shop/product_detail.html', title=product.name, product = product, current_user=current_user, cart=cart, addToCartForm = addToCartForm)

@bp.route('/sacola')
def shopping_cart():
    cart_manager = CartManager(session, current_user)
    print('CART = ', session['CART_ID'])
    cart = cart_manager.get_cart()
    return render_template('shop/shopping_cart.html', title='Minha Sacola', current_user=current_user, cart=cart)