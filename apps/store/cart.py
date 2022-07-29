from copy import copy
from typing import List, Tuple

from django.http import HttpRequest, QueryDict

from apps.store.forms import CartItemEditForm
from apps.store.models import Product


class Cart:

    def __init__(self, request: HttpRequest):
        self.request = request

    def add_cart_product(self, product: Product, quantity: int):
        if self.request.user.is_anonymous:
            self.add_product_in_session(product, quantity)
        if self.request.user.is_authenticated:
            self.request.user.cart.add_product()

    def add_cart_products(self, products: List[Tuple[Product, int]]):
        for product, quantity in products:
            self.add_cart_product(product, quantity)

    def get_cart_item(self) -> List[Tuple[Product, int]]:
        if self.request.user.is_anonymous:
            if "cart" not in self.request.session.keys():
                return []
            return self.convert_product_id_to_product()
        if self.request.user.is_authenticated:
            return list(self.request.user.cart.cartitem_set.all())

    def get_cart_item_count(self) -> int:
        if self.request.user.is_anonymous:
            if "cart" not in self.request.session.keys():
                return 0
            return len(self.request.session["cart"])
        if self.request.user.is_authenticated:
            return self.request.user.cart.cartitem_set.count()

    def edit_cat_item(self, post_data: QueryDict) -> bool:
        form = CartItemEditForm(post_data)
        if form.is_valid():
            if self.request.user.is_anonymous and self.request.session.get("cart"):
                self.edit_product_in_session(post_data)
            if self.request.user.is_authenticated:
                form.save_or_update()
            return True

    def convert_product_id_to_product(self):
        product_list = list()
        for product_pk, quantity in self.request.session["cart"]:
            product_list.append((Product.objects.filter(pk=product_pk).first(), quantity))
        return product_list

    def add_product_in_session(self, product: Product, quantity: int):
        if "cart" not in self.request.session.keys():
            last_cart = copy([])
        else:
            last_cart = copy(self.request.session["cart"])
        new_cart = list()
        if len(last_cart):
            for cart_product_id, cart_product_qty in last_cart:
                if product.id == cart_product_id:
                    new_cart.append([cart_product_id, cart_product_qty + quantity])
                else:
                    new_cart.append([cart_product_id, cart_product_qty])
        else:
            new_cart.append([product.id, quantity])
        self.request.session["cart"] = copy(new_cart)

    def edit_product_in_session(self, post_data: QueryDict):
        if post_data["request_type"] == "inc":
            self.add_product_in_session(post_data['product'], post_data['quantity'])

        if post_data["request_type"] == "dec":
            self.add_product_in_session(post_data['product'], (-1 * post_data['quantity']))

        if post_data["request_type"] == "del":
            cart_item.delete()
