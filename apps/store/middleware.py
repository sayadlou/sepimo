from django.contrib.sessions.models import Session

from apps.store.models import Cart


class CartMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(owner=request.user)
            Cart.objects.filter(session__session_key=request.session.session_key).delete()
        else:
            if not request.session.session_key:
                request.session.cycle_key()
            cart, _ = Cart.objects.get_or_create(session_id=request.session.session_key)
        request.cart = cart
        response = self.get_response(request)
        return response
