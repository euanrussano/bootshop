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