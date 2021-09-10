from flask_login import UserMixin
from app import db, login

from enum import unique
from hashlib import md5
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from slugify import slugify

from app.catalog.models import Product, ProductStock

class ShoppingCartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # -----------Relational fields-----------
    cart_id = db.Column(db.Integer, db.ForeignKey('shopping_cart.id'))
    product_stock_id = db.Column(db.Integer, db.ForeignKey('product_stock.id'))
    quantity = db.Column(db.Integer, default=1)
    price = db.Column(db.Numeric(scale=2), nullable=False)

    @property
    def product(self):
        product_stock = ProductStock.query.get(self.product_stock_id)
        product = Product.query.get(product_stock.product_id)
        return product

class ShoppingCart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # -----------Relational fields-----------
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    items = db.relationship('ShoppingCartItem', backref='cart', lazy=True)

    @property
    def total_price(self):
        return sum(item.price*item.quantity for item in self.items)

    @property
    def __len__(self):
        return len(self.items)

    def clear(self):
        for item in self.items:
            item.delete()

    