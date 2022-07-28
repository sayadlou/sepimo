from typing import List

from django.http import HttpRequest

from apps.store.models import Product


class Cart:

    def __init__(self, request: HttpRequest):
        self.request = request

    def add_cart_product(self, product: Product):
        if self.request.user.is_anonymous:
            if "cart" not in self.request.session.keys():
                self.request.session["cart"] = []
            self.request.session["cart"].append(product)
        if self.request.user.is_authenticated:
            self.request.user.cart.add_product()

    def add_cart_products(self, products: List[Product]):
        pass

    def get_cart_item(self) -> List[Product]:
        pass
