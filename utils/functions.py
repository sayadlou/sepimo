from apps.store.models import Cart, Order, OrderItem, CartItem


def cart_to_order(request):
    cart = request.user.cart
    order_items = list()
    new_order = Order.objects.create(owner=request.user, status='W')
    for item in cart.cartitem_set.all():
        order_items.append(
            OrderItem(
                order=new_order,
                quantity=item.quantity,
                product=item.product,
            )
        )
    OrderItem.objects.bulk_create(order_items, batch_size=20)
    return new_order


def print_attributes(obj):
    def attributes(obj):
        from inspect import getmembers
        from types import FunctionType
        disallowed_names = {
            name for name, value in getmembers(type(obj))
            if isinstance(value, FunctionType)}
        return {
            name: getattr(obj, name) for name in dir(obj)
            if name[0] != '_' and name not in disallowed_names and hasattr(obj, name)}


def copy_session_cart_to_user_cart(session_cart: Cart, user_cart: Cart):
    for cart_item in session_cart.cartitem_set.all():
        CartItem.objects.create(
            cart=user_cart,
            quantity=cart_item.quantity,
            product=cart_item.product,
        )
        print(cart_item)
