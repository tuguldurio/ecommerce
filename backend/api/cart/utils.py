from api.cart.models import Cart

def get_user_cart(user_id):
    ''' Get cart of current user '''
    return Cart.objects.get(user_id=user_id)