from django.contrib.auth import user_logged_in
from django.core.handlers.wsgi import WSGIRequest
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Cart
from ..account.models import UserProfile


@receiver(post_save, sender=UserProfile)
def create_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(owner=instance)


@receiver(user_logged_in)
def post_login(sender, user: UserProfile, request: WSGIRequest, **kwargs):
    try:
        cart = Cart.objects.get(session_key=request.session.session_key)
        cart.owner = user
        cart.save()
    except Cart.DoesNotExist:
        pass
