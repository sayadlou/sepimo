from django.contrib.auth import user_logged_in
from django.core.handlers.wsgi import WSGIRequest
from django.db.models.signals import post_save
from django.dispatch import receiver

from utils.functions import copy_session_cart_to_user_cart
from .models import Cart
from ..account.models import UserProfile


@receiver(post_save, sender=UserProfile)
def create_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(owner=instance)


@receiver(user_logged_in)
def post_login(sender, user: UserProfile, request: WSGIRequest, **kwargs):
    print("i log in")
    # cart = Cart.objects.get(session_key=request.session.session_key)
    print(request.session.session_key)
    session_cart = Cart.objects.get(session__session_key=request.session.session_key)
    print(session_cart)
    print(session_cart.cartitem_set.count())
    user_cart = Cart.objects.get(owner=user)
    copy_session_cart_to_user_cart(session_cart, user_cart)
    session_cart.delete()
