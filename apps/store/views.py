import logging
from copy import copy

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Avg, Count, Q, Max, Min
from django.db.models.functions import Coalesce
from django.forms import modelformset_factory
from django import forms
from django.http import HttpResponseBadRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django_filters.views import FilterView
from django.utils.translation import gettext as _

from .filters import ProductFilter
from .forms import ReviewForm, CartItemForm, WishItemForm, DiscountForm, OrderForm
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
        context['product_in_wishlist'] = [i for i in
                                          self.request.cart.wishitem_set.values_list('product_id', flat=True)]

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


class ProductView(View):
    model = Product
    template_name = 'store/product.html'
    review_form = ReviewForm
    success_url = reverse_lazy('store:product-code-slug')

    def get(self, request: WSGIRequest, *args, **kwargs):
        context = self.get_context_data()
        return render(request=self.request, template_name=self.template_name, context=context)

    def form_valid(self, form):
        messages.info(self.request, _('Review add'))
        form.save()
        return self.get(self.request)

    def form_invalid(self, form):
        messages.error(self.request, _('Review Not vaild'))
        context = self.get_context_data()
        context['form'] = form
        return render(request=self.request, template_name=self.template_name, context=context)

    def post(self, request: WSGIRequest, *args, **kwargs):
        form = self.review_form(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_form(self, form_class=None):
        return ReviewForm(self.request.Post)

    def get_object(self, queryset=None):
        code = self.kwargs.get('pk')
        return self.model.objects.filter(code=code).first()

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = {
            'product': self.get_object(),
            'reviews': self._get_reviews(),
            'title': self._get_page_title(),
            'same_products': self._get_same_product(),
            'next_product': self._get_next_product(),
            'prev_product': self._get_prev_product(),
            'form': self._get_review_form(),
            'product_in_wishlist': [i for i in self.request.cart.wishitem_set.values_list('product_id', flat=True)]}
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
    cart_item_formset = modelformset_factory(
        CartItem,
        extra=0,
        can_delete=True,
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

    def get(self, request: WSGIRequest, *args, **kwargs):
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return self.ajax_get(request, *args, **kwargs)
        return self.browser_get(request, *args, **kwargs)

    def post(self, request: WSGIRequest, *args, **kwargs):
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return self.ajax_post(request, *args, **kwargs)
        return self.browser_post(request, *args, **kwargs)

    def ajax_get(self, request: WSGIRequest, *args, **kwargs):
        return HttpResponse("OK")

    def ajax_post(self, request: WSGIRequest, *args, **kwargs):
        form = CartItemForm(request.POST)
        if form.is_valid():
            form.save_or_update()
            return HttpResponse("OK")
        return HttpResponseBadRequest("NOK")

    def browser_get(self, request: WSGIRequest, *args, **kwargs):
        formset = self.cart_item_formset(queryset=self.get_formset_initial_value)
        return render(request=self.request, template_name="store/cart.html", context=self.get_context(formset=formset))

    def browser_post(self, request: WSGIRequest, *args, **kwargs):
        formset = self.cart_item_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            messages.info(request, _('Cart Updated'))
            formset = copy(self.cart_item_formset(queryset=self.get_formset_initial_value))
        else:
            messages.error(request, _('Cart Not Valid'))
        return render(request=self.request, template_name="store/cart.html", context=self.get_context(formset=formset))

    @property
    def get_product_pictures(self):
        return self.request.cart.cartitem_set.values_list('product__introduction_picture__file', flat=True)

    @property
    def get_formset_initial_value(self):
        return self.request.cart.cartitem_set.all().order_by('id')

    def get_context(self, formset):
        form_initial = {
            "cart": self.request.cart.pk,
            "owner": self.request.user,
        }
        context = {
            "formset": formset,
            "product_pictures": self.get_product_pictures,
            "request": self.request,
            "shipping_list": Shipping.objects.all(),
            "cart_item": self.request.cart.cartitem_set.all(),
        }
        if self.request.user.is_authenticated:
            context["order_form"] = OrderForm(request=self.request, initial=form_initial)
            context["addresses"] = Address.objects.filter(owner=self.request.user)
        return context


class CartWidgetView(View):

    def get(self, request: WSGIRequest, *args, **kwargs):
        return render(request=self.request, template_name="store/cart_widget.html")


class WishList(View):
    template_name = 'store/whishlist.html'
    model = WishItem

    def get(self, request: WSGIRequest, *args, **kwargs):
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return self.ajax_get(request, *args, **kwargs)
        return self.browser_get(request, *args, **kwargs)

    def post(self, request: WSGIRequest, *args, **kwargs):
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return self.ajax_post(request, *args, **kwargs)
        return self.browser_post(request, *args, **kwargs)

    def ajax_get(self, request: WSGIRequest, *args, **kwargs):
        return HttpResponse("OK")

    def browser_get(self, request: WSGIRequest, *args, **kwargs):
        context = {
            'object_list': self.get_queryset(),
        }
        return render(request=request, template_name=self.template_name, context=context)

    def ajax_post(self, request: WSGIRequest, *args, **kwargs):
        form = WishItemForm(request.POST)
        if form.is_valid():
            form.save_or_update_existing()
            return HttpResponse(_("Product added to wish list"))
        return HttpResponseBadRequest(_("Product didn't add to wish list"))

    def browser_post(self, request: WSGIRequest, *args, **kwargs):
        return HttpResponse("OK")

    def get_queryset(self):
        return self.request.cart.wishitem_set.all()


class DiscountView(LoginRequiredMixin, View):
    model = Discount
    form = DiscountForm

    def post(self, request: WSGIRequest, *args, **kwargs):
        form = self.form(self.request.POST, request=request)
        if form.is_valid():
            return HttpResponse(f"{form.get_discount()}")
        else:
            print(form.errors)
            return HttpResponseNotFound("Not Found")


class OrderView(LoginRequiredMixin, View):
    def post(self, request: WSGIRequest, *args, **kwargs):
        form = OrderForm(request.POST, request=request)
        if form.is_valid():
            return HttpResponse(f"Valid")
        else:
            return HttpResponse(f"Not Valid")

    def get(self, request: WSGIRequest, *args, **kwargs):
        pass
