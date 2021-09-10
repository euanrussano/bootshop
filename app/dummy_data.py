from hashlib import md5
from werkzeug.security import generate_password_hash
from datetime import date
from random import randint

from app import db
# ------------------- User ---------------------------

from app.auth.models import User

emails = ['john@example.com', 'mary@example.com', 'carl@example.com', 'kevin@example.com', 'lisa@example.com']


User.query.delete()
for email in emails:

    u = User(email=email,
            is_staff=False)

    if email == "john@example.com":
        u.is_staff = True

    u.username = u.email.split('@')[0]
    u.set_password_hash("testing")
    
    db.session.add(u)

db.session.commit()

# ------------------- Address ---------------------------
from app.logistics.models import Address

addresses = [
    Address(
        address = 'Rua A',
        postal_code = 23894000,
        city = 'Cidade A',
        state = 'RJ',
        user_id = User.query.get(1).id
    ),
    Address(
        address = 'Rua B',
        postal_code = 23895000,
        city = 'Cidade A',
        state = 'RJ',
        user_id = User.query.get(1).id
    ),
    Address(
        address = 'Rua C',
        postal_code = 23897000,
        city = 'Cidade D',
        state = 'RJ',
        user_id = User.query.get(2).id
    ),
]

Address.query.delete()
for address in addresses:
    db.session.add(address)

db.session.commit()

# ------------------- Category ---------------------------
from app.catalog.models import Category
category_names = ['Categoria A', 'Categoria B', 'Categoria C']

Category.query.delete()
for category_name in category_names:
    cat = Category(name=category_name)

    db.session.add(cat)

db.session.commit()

# ------------------- Products ---------------------------
from app.catalog.models import Product

products =[
    Product(
    name = 'Produto 1',
    description = 'A simple product ',
    category_id = 1),
    
    Product(
    name = 'Produto 2',
    description = 'Another simple product ',
    category_id = 1),

    Product(
    name = 'Produto 3',
    description = 'Even another simple product ',
    category_id = 2)
]

Product.query.delete()
for product in products:
    db.session.add(product)

db.session.commit()


def get_products_perc_month():
    return 11

# ------------------- Review ---------------------------
from app.catalog.models import ProductReview

product_reviews = [
    ProductReview(
        description = 'Excellent product',
        product_id = Product.query.get(1).id,
        user_id = User.query.get(1).id,
        rating = 5
    ),
    ProductReview(
        description = 'Worst product ever',
        product_id = Product.query.get(2).id,
        user_id = User.query.get(2).id,
        rating = 1
    ),
    ProductReview(
        description = 'Average but ok, no problem.',
        product_id = Product.query.get(2).id,
        user_id = User.query.get(3).id,
        rating = 3
    ),
    ProductReview(
        description = 'Good product',
        product_id = Product.query.get(3).id,
        user_id = User.query.get(3).id,
        rating = 4
    ),
]

ProductReview.query.delete()
for review in product_reviews:
    db.session.add(review)

db.session.commit()

# ------------------- Product Stock ---------------------------
from app.catalog.models import ProductStock

product_stocks = [
    ProductStock(
    product_id = Product.query.get(1).id,
    quantity = 10,
    quantity_sold = 0,
    price = 1.99,
    price_acquired=0.99),

    ProductStock(
    product_id = Product.query.get(1).id,
    quantity = 13,
    quantity_sold = 3,
    price = 12.99,
    price_acquired=11.99)
]

ProductStock.query.delete()
for product_stock in product_stocks:
    db.session.add(product_stock)

db.session.commit()

# ------------------- Wishlist ---------------------------

from app.catalog.models import Wishlist, products_wishlist

wishlists = [
    Wishlist(
        user_id = User.query.get(1).id
    )
]

Wishlist.query.delete()
for wishlist in wishlists:
    db.session.add(wishlist)

db.session.commit()

#products_wishlist.delete()
#ins = products_wishlist.insert().values(product_id=1, wishlist_id=1)
#db.engine.execute(ins)

# ------------------- Orders ---------------------------

from app.logistics.models import OrderItem, Order

orders = [
    Order(
        user_id = User.query.get(1).id
    )
]

Order.query.delete()
for order in orders:
    db.session.add(order)

db.session.commit()

order_items = [
    OrderItem(
        productstock_id = ProductStock.query.get(1).id,
        quantity = 2,
        price = ProductStock.query.get(1).price,
        order_id = Order.query.get(1).id
    ),
    OrderItem(
        productstock_id = ProductStock.query.get(2).id,
        quantity = 1,
        price = ProductStock.query.get(2).price,
        order_id = Order.query.get(1).id
    ),

]

OrderItem.query.delete()
for i, order_item in enumerate(order_items):
    db.session.add(order_item)

db.session.commit()



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
