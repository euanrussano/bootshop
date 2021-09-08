from flask_login import UserMixin
from app import db, login

from enum import unique
from hashlib import md5
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(120), nullable=False)
    postal_code = db.Column(db.Integer, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    # -----------Relational fields-----------
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    paid = db.Column(db.Boolean)
    # -----------Relational fields-----------
    order_items = db.relationship('OrderItem', backref='order', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Order from user {} with order items {}>'.format(self.user_id, self.order_items)


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Numeric(scale=2))
    quantity = db.Column(db.Integer, default = 0)
    # -----------Relational fields-----------
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    productstock_id = db.Column(db.Integer, db.ForeignKey('product_stock.id'))

    def __repr__(self):
        return '<OrderItem of product {} in order {}>'.format(self.product_id, self.order_id)