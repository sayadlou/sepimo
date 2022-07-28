from apps.store.Cart import Cart


class CartMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        request.cart = Cart(request)
        response = self.get_response(request)
        return response


