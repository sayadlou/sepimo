from datetime import timedelta, datetime
from decimal import Decimal
from pprint import pprint
from time import mktime

import os
import requests
import json
from uuid import uuid4
import logging

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.utils.translation import gettext as _
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .forms import CartItemForm
from .models import *
from config.settings.base import MINIMUM_ORDER_AMOUNT

logger = logging.getLogger('store.views')


class CartListAddView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        context = {'cart': request.user.cart}
        cart_has_item = CartItem.objects.filter(cart=request.user.cart).exists()
        context['cart_has_item'] = cart_has_item
        if cart_has_item:
            context['cart_item'] = CartItem.objects.filter(cart=request.user.cart).order_by('id')
            cart_sum = 0
            for item in context['cart_item']:
                cart_sum += item.product.price * Decimal(item.quantity)
            context['cart_sum'] = cart_sum
        return render(request=self.request, template_name="store/cart.html", context=context)

    def post(self, request, *args, **kwargs):
        post_copy = request.POST.copy()
        post_copy['cart'] = self.request.user.cart
        form = CartItemForm(data=post_copy)
        if form.is_valid():
            messages.success(request, _('product added to cart'))
            form.save_or_update()
        else:
            for key in form.errors:
                for error in form.errors[key]:
                    messages.error(request, error)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class CartPutDeleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        cart_item = get_object_or_404(CartItem, pk=kwargs['pk'])
        post_copy = request.POST.copy()
        post_copy['cart'] = self.request.user.cart
        form = CartItemForm(data=post_copy, instance=cart_item)
        if form.is_valid():
            messages.success(request, _('product updated'))
            form.save_or_update()
        else:
            for key in form.errors:
                for error in form.errors[key]:
                    messages.error(request, error)
        return redirect(reverse('store:cart'), permanent=True)

    def delete(self, request, *args, **kwargs):
        obj = get_object_or_404(CartItem, pk=kwargs['pk'])
        if request.user.cart.pk == obj.cart.pk:
            obj.delete()
            return HttpResponse("deleted")
        else:
            return HttpResponse(status=404)


class OrderListView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        orders = Order.objects.filter(owner=request.user)
        context = {'orders': orders, 'has_order': orders.exists()}
        return render(request=self.request, template_name="store/orders.html", context=context)


class OrderDetailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order, owner=request.user, pk=kwargs["pk"])
        context = {'order': order}
        return render(request=request, template_name="store/order.html", context=context)


class PaymentListAddView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        payments = Payment.objects.filter(owner=request.user)
        context = {'payments': payments, 'has_payments': payments.exists()}
        return render(request=self.request, template_name="store/payments.html", context=context)

    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            pass
            # order_id = request.POST.get('order_id')
            # try:
            #     order = Order.objects.get(owner=request.user, pk=order_id)
            # except Order.DoesNotExist:
            #     order = self.cart_to_order(request)
            # if order.total_price <= MINIMUM_ORDER_AMOUNT:
            #     messages.success(request, _('minimum order amount should be more than 100,000 IRR'))
            #     return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            # request.user.cart.cartitem_set.all().delete()
            # factory = bankfactories.BankFactory()
            # try:
            #     bank = factory.auto_create(bank_models.BankType.ZARINPAL)
            #     bank.set_request(request)
            #     bank.set_amount(int(order.total_price))
            #     bank.set_client_callback_url(reverse_lazy('store:callback-gateway'))
            #     bank.set_mobile_number(order.owner.mobile)
            #     bank_record = bank.ready()
            #     Payment.objects.create(
            #         owner=request.user,
            #         order=order,
            #         amount=(int(order.total_price)),
            #         transaction=bank_record,
            #     )
            #     return bank.redirect_gateway()
            # except AZBankGatewaysException as e:
            #     logging.critical(e)
            #     # TODO: redirect to failed page.
            #     raise e

    def cart_to_order(self):
        if not self.request.user.cart.cartitem_set.exists():
            raise HttpResponseBadRequest
        cart = self.request.user.cart
        order_items = list()
        new_order = Order.objects.create(owner=self.request.user, status='W')
        for item in cart.cartitem_set.all():
            order_items.append(
                OrderItem(
                    order=new_order,
                    quantity=item.quantity,
                    product=item.product,
                )
            )
        OrderItem.objects.bulk_create(order_items, batch_size=20)
        return new_order


# class CallbackGatewayView(LoginRequiredMixin, View):
#
#     def get(self, request, *args, **kwargs):
#         tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
#         if not tracking_code:
#             logging.error("tracking code is not in url query param.")
#             raise Http404
#         try:
#             bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
#         except bank_models.Bank.DoesNotExist:
#             logging.error("bank record is not valid")
#             raise Http404
#         if bank_record.is_success:
#             try:
#                 payment = Payment.objects.get(content_type=ContentType.objects.get_for_model(bank_record),
#                                               object_id=bank_record.pk)
#                 payment.status = Payment.STATUS_CONFIRMED
#                 payment.save()
#                 payment.order.status = Order.ORDER_STATUS_PAYED
#                 payment.order.save()
#                 paid_order_items = payment.order.orderitem_set.all()
#                 bayer = payment.owner
#                 for item in paid_order_items:
#                     item.product.add_buyer(bayer)
#                 return HttpResponse("پرداخت با موفقیت انجام شد.")
#             except Payment.DoesNotExist:
#                 logging.error(f"payment for {bank_record.pk} was successful but has no oder")
#                 return HttpResponse("خطایی در پرداخت رخ داده است جهت بازپرداخت وجه با پشتیبانی تماس حاصل نمایید.")
#         logging.error(f"payment {bank_record.pk} with amount {bank_record.amount} was not successful")
#         return HttpResponse(
#             "پرداخت با شکست مواجه شده است.اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.")


