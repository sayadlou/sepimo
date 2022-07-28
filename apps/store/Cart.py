from copy import copy
from typing import List, Tuple

from django.http import HttpRequest

from apps.store.models import Product


class Cart:

    def __init__(self, request: HttpRequest):
        self.request = request

    def add_cart_product(self, product: Product, quantity: int):
        # if self.request.user.is_anonymous:
        #     if "cart" not in self.request.session.keys():
        #         self.request.session["cart"] = []
        #     print(type(self.request.session["cart"]))
        #
        #     self.request.session["cart"].append((product, quantity))
        if self.request.user.is_anonymous:
            if "cart" not in self.request.session.keys():
                last_cart = copy([])
            else:
                last_cart = copy(self.request.session["cart"])
            last_cart.append([product.pk, quantity])
            self.request.session["cart"] = copy(last_cart)
        if self.request.user.is_authenticated:
            self.request.user.cart.add_product()

    def add_cart_products(self, products: List[Tuple[Product, int]]):
        for product, quantity in products:
            self.add_cart_product(product, quantity)

    def get_cart_item(self) -> List[Tuple[Product, int]]:
        if self.request.user.is_anonymous:
            if "cart" not in self.request.session.keys():
                return []
            return self.convert_session_product()
        if self.request.user.is_authenticated:
            return list(self.request.user.cart.cartitem_set.all())

    def convert_session_product(self):
        product_list = list()
        for product_pk, quantity in self.request.session["cart"]:
            product_list.append((Product.objects.filter(pk=product_pk).first(), quantity))
        return product_list
