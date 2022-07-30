from django.core.handlers.wsgi import WSGIRequest

from .models import Cart


def cart_processor(request: WSGIRequest):

    context = {
        'foo': 'bar',
        'cart': "cart"
    }
    return context
