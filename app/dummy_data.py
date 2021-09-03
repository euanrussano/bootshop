from hashlib import md5
from werkzeug.security import generate_password_hash
from datetime import date
from random import randint

from app import db
# ------------------- Users ---------------------------

from app.models import Category, Product, ProductReview, ProductStock, User

emails = ['john@example.com', 'mary@example.com', 'carl@example.com', 'kevin@example.com', 'lisa@example.com']


for email in emails:
    if not User.query.filter_by(email=email).all():
        u = User(email=email,
                is_staff=False)

        if email == "john@example.com":
            u.is_staff = True

        u.username_from_email()
        u.set_password_hash("testing")
        
        db.session.add(u)

db.session.commit()

# ------------------- Category ---------------------------

category_names = ['Categoria A', 'Categoria B', 'Categoria C']

for category_name in category_names:
    if not Category.query.filter_by(name=category_name).all():
        cat = Category(name="Categoria A")

        db.session.add(cat)

# ------------------- Products ---------------------------

products =[
    Product(
    name = 'Produto 1',
    price = 12.99,
    description = 'A simple product ',
    available = True,
    category_id = 1),
    
    Product(
    name = 'Produto 2',
    price = 2.30,
    description = 'Another simple product ',
    available = True,
    category_id = 1),

    Product(
    name = 'Produto 3',
    price = 8.25,
    description = 'Even another simple product ',
    available = True,
    category_id = 2)
]

for product in products:
    if not Product.query.filter_by(name=product.name).all():
        db.session.add(product)

db.session.commit()


def get_products_perc_month():
    return 11

# ------------------- Product Stock ---------------------------

product_stocks = [
    ProductStock(
    product_id = Product.query.get(1).id,
    user_id = User.query.get(1).id,
    quantity = 10,
    quantity_sold = 0),

    ProductStock(
    product_id = Product.query.get(1).id,
    user_id = User.query.get(2).id,
    quantity = 13,
    quantity_sold = 3)
]

for product_stock in product_stocks:
    if not ProductStock.query.filter_by(quantity=product_stock.quantity).all():
        db.session.add(product_stock)

db.session.commit()


# ------------------- Messages ---------------------------
Message = [
            {'user': User.query.get(1),
             'text':'test message 1'},
            {'user': User.query.get(1),
             'text':'test message 2'},
                         ]

# ------------------- Notifications ---------------------------
Notification = [
        {'text': '8 emails'},
        {'text': '4 new contacts'},
    ]

# ------------------- Review ---------------------------

product_reviews = [
    ProductReview(
        description = 'Excellent product',
        product_id = Product.query.get(1),
        user_id = User.query.get(1),
        rating = 5
    ),
    ProductReview(
        description = 'Worst product ever',
        product_id = Product.query.get(2),
        user_id = User.query.get(2),
        rating = 1
    ),
    ProductReview(
        description = 'Average but ok, no problem.',
        product_id = Product.query.get(2),
        user_id = User.query.get(3),
        rating = 3
    ),
    ProductReview(
        description = 'Good product',
        product_id = Product.query.get(3),
        user_id = User.query.get(3),
        rating = 4
    ),
]

for review in product_reviews:
    if not ProductReview.query.filter_by(description=review.description).all():
        db.session.add(review)

db.session.commit()

# ------------------- Orders ---------------------------


Order = [
    {
        'user': User.query.get(1),
        'products':[Product.query.get(1)],
    },
    {
        'user': User.query.get(1),
        'products':[Product.query.get(1), Product.query.get(2)],
    }
]

def get_total_cost(order):
    return sum( list(map( lambda product: product.price, order['products'])) )


def get_orders_total():
    cost = 0
    for order in Order:
        cost += get_total_cost(order)

    return cost

def get_orders_perc_month():
    return 11

def get_best_selling_products():
    order_products_count = {}
    for order in Order:
        for product in order['products']:
            if product.id in order_products_count:
                order_products_count[product.id] += 1
            else:
                order_products_count[product.id] = 1


    best_selling_product = [Product.query.get(product_id) for product_id, count in sorted(order_products_count.items(), key=lambda item: item[1])][-3:]
    return best_selling_product



