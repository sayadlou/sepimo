import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Avg, Count, Q, Max, Min
from django.db.models.functions import Coalesce
from django.forms import modelformset_factory
from django import forms
from django.http import HttpResponseBadRequest, HttpResponse, QueryDict
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView
from django_filters.views import FilterView
from django.utils.translation import gettext as _

from .filters import ProductFilter
from .forms import ReviewForm, CartItemEditForm
from .models import *

logger = logging.getLogger('store.views')


class ProductListView(FilterView):
    model = Product
    paginate_by = 8
    template_name = 'store/product_list.html'
    filterset_class = ProductFilter

    def __init__(self, *args, **kwargs):
        self.min_price: int = 0
        self.max_price: int = 99999999
        self.order_strategy = {
            "date": {
                "name": "تاریخ",
                "orm_arg": "created_at"
            },
            "rating": {
                "name": "امتیاز",
                "orm_arg": "rate"
            },
            "popularity": {
                "name": "محبوبیت",
                "orm_arg": "sold"
            },

        }

        super().__init__(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['category'] = self.get_category_filter()
        context['brand'] = self.get_brand_filter()
        context['price_min'] = self.get_price_min_filter_default()
        context['price_max'] = self.get_price_max_filter_default()
        context['price_lte'] = self.get_price_lte_filter_default()
        context['price_gte'] = self.get_price_gte_filter_default()
        context['order_strategy'] = self.order_strategy
        context['total_product'] = self.get_queryset().count()
        context['paginate_by'] = self.paginate_by
        print(self.request.cart.cartitem_set.all())

        return context

    def get_category_filter(self):
        categories_name = Category.objects.values_list('name', flat=True)
        categories_filter: list = []
        for category_name in categories_name:
            categories_filter.append({
                'name': "category",
                'value': category_name,
                'count': Product.objects.filter(category__name=category_name).count(),
                'check': 'checked' if category_name in self.request.GET.getlist('category') else '',
            })
        return categories_filter

    def get_brand_filter(self):
        brands_name = Brand.objects.values_list('name', flat=True)
        brands_filter: list = []
        for brand_name in brands_name:
            brands_filter.append({
                'name': "brand",
                'value': brand_name,
                'count': Product.objects.filter(brand__name=brand_name).count(),
                'check': 'checked' if brand_name in self.request.GET.getlist('brand') else '',
            })
        return brands_filter

    def get_price_max_filter_default(self):
        max_price_dict = Product.objects.aggregate(Max('price'))
        max_price = max_price_dict.get('price__max', 9999999999999)
        self.max_price = int(max_price)
        return self.max_price

    def get_price_min_filter_default(self):
        min_price_dict = Product.objects.aggregate(Min('price'))
        min_price = min_price_dict.get('price__min', 0)
        self.min_price = int(min_price)
        return self.min_price

    def get_price_gte_filter_default(self):
        default = self.min_price
        price_gte = self.request.GET.get('price_gte', default)
        price_gte = default if price_gte == "" else price_gte
        return price_gte

    def get_price_lte_filter_default(self):
        default = self.max_price
        price_lte = self.request.GET.get('price_lte', default)
        price_lte = default if price_lte == "" else price_lte
        return price_lte

    def get_queryset(self):
        return self.model.objects.filter(status='Published') \
            .annotate(rate=Coalesce(Avg("review__rate"), 0.0)) \
            .annotate(reviws=Count("review", filter=Q(review__status='Published'))) \
            .order_by(self.get_order_parameter())

    def get_order_parameter(self):
        orm_arg = "pk"
        requested_order = self.request.GET.get("sortby")
        strategy = self.order_strategy.get(requested_order)
        if strategy:
            orm_arg = strategy["orm_arg"]
        return orm_arg


class ProductView(DetailView):
    model = Product
    template_name = 'store/product.html'
    review_form = ReviewForm

    def get_object(self, queryset=None):
        code = self.kwargs.get('pk')
        return self.model.objects.filter(code=code).first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['reviews'] = self._get_reviews()
        context['title'] = self._get_page_title()
        context['same_products'] = self._get_same_product()
        context['next_product'] = self._get_next_product()
        context['prev_product'] = self._get_prev_product()
        context['form'] = self._get_review_form()
        context['product_form'] = CartItemEditForm(
            initial={"cart": self.request.cart, "product": self.object, "request_type": "add", "quantity": 1})
        return context

    def _get_review_form(self):
        return self.review_form(initial={"product": self.object})

    def _get_page_title(self):
        return self.object.title

    def _get_same_product(self):
        return self.model.objects.filter(category=self.object.category).filter(status='Published') \
            .annotate(rate=Coalesce(Avg("review__rate"), 0.0)) \
            .annotate(reviws=Count("review", filter=Q(review__status='Published'))) \
            .exclude(pk=self.object.pk)

    def _get_reviews(self):
        return self.object.review_set.filter(status='Published').filter(
            language=self.request.LANGUAGE_CODE)

    def _get_next_product(self):
        return self.model.objects.order_by('id').filter(category=self.object.category).filter(
            id__gt=self.object.id).first()

    def _get_prev_product(self):
        return self.model.objects.order_by('id').filter(category=self.object.category).filter(
            id__lt=self.object.id).last()


class CartView(View):
    cart_item_formset = modelformset_factory(CartItem, extra=0, can_delete=True,
                                             fields=['cart', 'quantity', 'product', ],
                                             widgets={
                                                 "cart": forms.TextInput(
                                                     attrs={'class': 'form-control mt-0 mb-0 d-none'}),
                                                 "quantity": forms.TextInput(
                                                     attrs={'class': 'form-control mt-0 mb-0 cart_qty'}),
                                                 "product": forms.TextInput(
                                                     attrs={'class': 'form-control mt-0 mb-0 d-none'}),
                                             }
                                             )

    def get(self, request, *args, **kwargs):
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return self.ajax_get(request, *args, **kwargs)
        return self.browser_get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return self.ajax_post(request, *args, **kwargs)
        return self.browser_post(request, *args, **kwargs)

    def ajax_get(self, request, *args, **kwargs):
        print("ajax get")
        return HttpResponse("OK")

    def ajax_post(self, request, *args, **kwargs):
        form = CartItemEditForm(request.POST)
        if form.is_valid():
            form.save_or_update()
            return HttpResponse("OK")
        else:
            print(form.errors.as_text)
        return HttpResponseBadRequest("NOK")

    def browser_get(self, request, *args, **kwargs):
        formset = self.cart_item_formset(queryset=self.get_formset_initial_value)
        product_pictures = self.get_product_pictures
        context = {
            "formset": formset,
            "product_pictures": product_pictures,
        }
        return render(request=self.request, template_name="store/cart.html", context=context)

    def browser_post(self, request, *args, **kwargs):
        print("normal post")
        # Check if submitted forms are valid
        formset = self.cart_item_formset(data=request.POST)
        product_pictures = self.get_product_pictures
        if formset.is_valid():
            formset.save()
            messages.info(request, _('Cart Updated'))
            formset = self.cart_item_formset(queryset=self.get_formset_initial_value)
        else:
            messages.error(request, _('Cart Not Valid'))
        context = {
            "formset": formset,
            "product_pictures": product_pictures,
        }
        return render(request=self.request, template_name="store/cart.html", context=context)

    @property
    def get_product_pictures(self):
        return self.request.cart.cartitem_set.values_list('product__introduction_picture__file', flat=True)

    @property
    def get_formset_initial_value(self):
        return self.request.cart.cartitem_set.all().order_by('id')


class CartWidgetView(View):

    def get(self, request, *args, **kwargs):
        return render(request=self.request, template_name="store/cart_widget.html")


class WishList(ListView):
    template_name = 'store/whishlist.html'
    model = WishItem

    def get_queryset(self):
        return self.request.cart.wishitem_set.all()


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
