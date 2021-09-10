from app.shop.models import ShoppingCartItem, ShoppingCart
from app import db

class CartManager:
    def __init__(self, session, current_user):
        self.session = session
        
        shopping_cart = None
        # check if there is already cart_id in session
        if 'CART_ID' in session:
            shopping_cart = ShoppingCart.query.get(session['CART_ID'])
        
        # if there is no cart_id but the user is auth, try to get his shopping cart
        if current_user.is_authenticated:
            shopping_cart = ShoppingCart.query.filter_by(user_id = current_user.id).first()
                
        # if there is no session cart_id and the user is not authenticated and the user has no shopping cart, create
        # a new one
        
        if shopping_cart is None:
            shopping_cart = ShoppingCart()

        # make sure the shopping cart is associated with authenticaded user (for new users)
        if current_user.is_authenticated:
            shopping_cart.user_id = current_user.id

        print('shopping Cart ID', shopping_cart.id)
        session['CART_ID'] = shopping_cart.id
        self.cart = shopping_cart
        

        db.session.add(shopping_cart)
        db.session.commit()

    def get_cart(self): 
        return self.cart

    def add(self, product_stock, quantity, override_quantity=False):
        
        item = [item for item in self.cart.items if item.product_stock_id == product_stock.id]
        if not item:
            item = ShoppingCartItem(cart_id = self.cart.id,
                                    product_stock_id = product_stock.id,
                                    quantity = quantity,
                                    price = product_stock.price)
            
            db.session.add(item)

        else:
            item = item[0]
        
        if override_quantity:
            item.quantity = quantity
        else:
            item.quantity += quantity

        
        db.session.commit()
    
    def remove(self, product_stock):
        item = self.cart.items.filter_by(product_stock_id = product_stock.id).first()
        if item:
            item.delete()

        db.session.commit()
    
    def transfer_to_user(self, user):
        if self.cart.user_id and self.cart_user_id != user.id:
            return False
        self.cart.user_id = user.id

        db.session.commit()




