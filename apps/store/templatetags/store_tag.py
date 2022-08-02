from django import template
from django.http import QueryDict
from django.utils.safestring import mark_safe

from apps.store.models import CartItem

register = template.Library()


@register.simple_tag(takes_context=True)
def print_fild(context, counter, arg=None):
    print(context["product_pic_url"][0], counter)
    url = context["product_pic_url"][counter]
    return mark_safe(f'<img src="/media/{url}">')


@register.simple_tag(takes_context=True)
def get_product_attr(context, attribute: str, index: int, arg=None):
    cart_items: QueryDict[CartItem] = context["request"].cart.cartitem_set.all()
    cart_item = cart_items[index]
    product = cart_item.product
    return getattr(product, attribute)


@register.simple_tag(takes_context=True)
def get_product_picture(context, index: int, arg=None):
    cart_items: QueryDict[CartItem] = context["request"].cart.cartitem_set.all()
    cart_item = cart_items[index]
    product = cart_item.product
    return getattr(product, "introduction_picture").url


@register.simple_tag(takes_context=True)
def get_cartitem_total_price(context, index: int, arg=None):
    cart_items: QueryDict[CartItem] = context["request"].cart.cartitem_set.all()
    cart_item = cart_items[index]
    return cart_item.get_cartitem_total_price
