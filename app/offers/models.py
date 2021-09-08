from datetime import datetime

from app import db

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