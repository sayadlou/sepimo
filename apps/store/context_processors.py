from django.core.handlers.wsgi import WSGIRequest

from .models import Cart


def cart_processor(request: WSGIRequest):
    if request.user.is_authenticated:
        cart = Cart.objects.get_or_create(owner=request.user)
        Cart.objects.filter(session_key__session_key=request.session.session_key).delete()
    else:
        cart = Cart.objects.get_or_create(session_key__session_key=request.session.session_key)
    context = {
        'foo': 'bar',
        'cart': cart
    }
    return context
