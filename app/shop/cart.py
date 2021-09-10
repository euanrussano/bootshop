from app.shop.models import ShoppingCartItem, ShoppingCart

class CartManager:
    def __init__(self, session, current_user):
        self.session = session
        
        shopping_cart = None
        # check if there is already cart_id in session
        if 'CART_ID' in session:
            shopping_cart = ShoppingCart.query.get(session['CART_ID'])
        # if there isn't but the user is auth, try to get his shopping cart
        elif current_user.is_authenticated:
            shopping_cart = ShoppingCart.query.filter_by(user_id = current_user.id).first()
                
        # if there is no session cart_id and the user is not authenticated and the user has no shopping cart, create
        # a new one
        if not shopping_cart:
            shopping_cart = ShoppingCart()
        
        session['CART_ID'] = shopping_cart.id
        self.cart = shopping_cart

    def get_cart(self): 
        return self.cart

    def add(self, product_stock, quantity, override_quantity=False):
        
        item = self.cart.items.filter_by(product_stock_id = product_stock.id).first()
        if not item:
            item = ShoppingCartItem(cart_id = self.cart.id,
                                    product_stock_id = product_stock.id,
                                    quantity = quantity,
                                    price = product_stock.price)
        else:
            if override_quantity:
                item.quantity = quantity
            else:
                item.quantity += quantity
    
    def remove(self, product_stock):
        item = self.cart.items.filter_by(product_stock_id = product_stock.id).first()
        if item:
            item.delete()
    
    def transfer_to_user(self, user):
        if self.cart.user_id and self.cart_user_id != user.id:
            return False
        self.cart.user_id = user.id




