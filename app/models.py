from flask_login import UserMixin
from app import db, login

from enum import unique
from hashlib import md5
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))
    is_staff = db.Column(db.Boolean, default=False)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)
    # -----------Relational fields-----------
    product_reviews = db.relationship('ProductReview', backref='user', lazy=True)
    addresses = db.relationship('Address', backref='user', lazy=True)
    orders = db.relationship('Order', backref='user', lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def username_from_email(self):
        self.username = self.email.split('@')[0]

    @property
    def avatar(self):
        size_avatar = 128
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(md5((self.email).lower().encode('utf-8')).hexdigest(), size_avatar)

    def set_password_hash(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password_hash(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

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

class Category(db.Model):
    # TODO: add subcategory
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    # -----------Relational fields-----------
    products = db.relationship('Product', backref='category', lazy=True)

    def __repr__(self):
        return '<Category {}>'.format(self.name)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(2000))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # -----------Relational fields-----------
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    #product_stocks = db.relationship('ProductStock', backref='product', lazy=True)
    product_reviews = db.relationship('ProductReview', backref='product', lazy=True)
    product_images = db.relationship('ProductImage', backref='product', lazy=True)

    @property
    def total_stock(self):
        return ProductStock.total_stock_by_product(self)
    
    @property
    def thumbnail(self):
        size_avatar = 128
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(md5((self.name).lower().encode('utf-8')).hexdigest(), size_avatar)

    @property
    def category(self):
        return Category.query.get(self.category_id)

    def __repr__(self):
        return '<Product {}>'.format(self.name)


class ProductReview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(2000))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    rating = db.Column(db.Integer)
    # -----------Relational fields-----------
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    

    def __repr__(self):
        return '<Review of product {} from user {}>'.format(self.product_id, self.user_id)

class ProductStock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    quantity = db.Column(db.Integer, default = 0)
    price_acquired = db.Column(db.Numeric(scale=2))
    price = db.Column(db.Numeric(scale=2))
    available = db.Column(db.Boolean)
    quantity_sold = db.Column(db.Integer, default = 0)
    # -----------Relational fields-----------
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    order_items = db.relationship('OrderItem', backref='product_stock', lazy=True)

    def __repr__(self):
        return '<Stock of product {} from user {} with quantity not sold {} and sold {}>'.format(self.product_id, self.user_id, self.quantity, self.quantity_sold)

    @staticmethod
    def total_stock_by_product(product):
        product_id = product.id
        product_stocks = ProductStock.query.filter_by(product_id = product_id).all()
        total_stock = sum(ps.quantity for ps in product_stocks)

        return total_stock


products_wishlist = db.Table('products_wishlist',
    db.Column('wishlist_id', db.Integer, db.ForeignKey('wishlist.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
)

class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # -----------Relational fields-----------
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    products = db.relationship('Product', secondary=products_wishlist, lazy='subquery',
        backref=db.backref('wishlists', lazy=True))


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


class ProductImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(64))
    image_filename = db.Column(db.String(64))
    alt_text = db.Column(db.String(64))
    caption = db.Column(db.String(128))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

    def __repr__(self):
        return '<ProductImage {} - {}>'.format(self.url, self.caption)

class Offer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expire_at = db.Column(db.DateTime, nullable=True)
    offer_type = db.Column(db.String(64))
    number_vouchers = db.Column(db.Integer)
    motivation = db.Column(db.String(64))
    condition = db.Column(db.String(64))
    available = db.Column(db.Boolean)
    usage = db.Column(db.Integer)
    cost = db.Column(db.Numeric(scale=2))

products_coupon = db.Table('products_coupon',
    db.Column('discount_coupon_id', db.Integer, db.ForeignKey('discount_coupon.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
)

class DiscountCoupon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    code = db.Column(db.String(64))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expire_at = db.Column(db.DateTime, nullable=True)
    
    # STSC - Can be used one Single Time for one Single Client
    # MTMC - Can be used Multiple Times for Multiple Clients
    # STMC - Can be used one Single Time for Multiple Clients
    usage = db.Column(db.String(2)) 
    # -----------Relational fields-----------
    products = db.relationship('Product', secondary=products_coupon, lazy='subquery',
        backref=db.backref('discount_coupons', lazy=True))









