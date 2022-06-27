import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.utils.translation import gettext as _
from django.views import View
from vanilla import ListView, DetailView

from .forms import CartItemForm
from .models import *

logger = logging.getLogger('store.views')


class ProductView(DetailView):
    model = Product
    template_name = 'store/product.html'
    lookup_url_kwarg = 'code'


class ProductsView(ListView):
    model = Product
    template_name = 'store/products.html'


class CartView(ListView):
    model = Cart


class CartApiView(View):

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


class WishListView(ListView):
    pass


class WishListApiView(View):
    pass
