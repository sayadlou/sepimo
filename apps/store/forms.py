from captcha.fields import CaptchaField
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from .models import *
from .widget import CustomCaptchaTextInput


class CartItemForm(forms.ModelForm):
    request_type = forms.CharField(max_length=3, required=True)

    class Meta:
        model = CartItem
        fields = ['cart', 'quantity', 'product', 'request_type']

    def clean(self):
        cleaned_post_data = super().clean()
        product = cleaned_post_data['product']
        if not cleaned_post_data["request_type"] in ("dec", "inc", 'del', 'add'):
            raise ValidationError(_("requested type is not valid"))
        if cleaned_post_data["request_type"] != "add":
            try:
                data = CartItem.objects.get(product=product.id)
                if cleaned_post_data["request_type"] == "inc":
                    if data.quantity + cleaned_post_data['quantity'] > product.maximum_order_quantity:
                        raise ValidationError(_("quantity is more than allowed value"))
                if cleaned_post_data["request_type"] == "dec":
                    if data.quantity - cleaned_post_data['quantity'] < product.minimum_order_quantity:
                        raise ValidationError(_("quantity is less than allowed value"))

            except CartItem.DoesNotExist:
                raise ValidationError(_("product not found"))

    def save_or_update(self):
        if self.cleaned_data["request_type"] == "add":
            try:
                cart_item = self.Meta.model.objects.get(cart=self.cleaned_data["cart"],
                                                        product=self.cleaned_data["product"])
                cart_item.quantity += self.instance.quantity
                cart_item.save()
            except CartItem.DoesNotExist:
                self.save()
            except CartItem.MultipleObjectsReturned:
                cart_items_sum = CartItem.objects \
                    .filter(cart=self.cleaned_data["cart"], product=self.cleaned_data["product"]) \
                    .aggregate(Sum('quantity'))
                self.Meta.model.objects.filter(cart=self.cleaned_data["cart"],
                                               product=self.cleaned_data["product"]).delete()
                self.instance.quantity += cart_items_sum["quantity__sum"]
                super().save()
        else:
            cart_item = CartItem.objects.get(product=self.cleaned_data['product'])
            if self.cleaned_data["request_type"] == "inc":
                cart_item.quantity += self.cleaned_data['quantity']
                cart_item.save()

            if self.cleaned_data["request_type"] == "dec":
                cart_item.quantity -= self.cleaned_data['quantity']
                cart_item.save()

            if self.cleaned_data["request_type"] == "del":
                cart_item.delete()


class WishItemForm(forms.ModelForm):
    actions = (
        ("add", "add"),
        ("del", "del"),
    )
    request_type = forms.ChoiceField(required=True, choices=actions)

    class Meta:
        model = WishItem
        fields = ['cart', 'product', 'request_type']

    def save_or_update_existing(self):
        if self.cleaned_data["request_type"] == "add":
            try:
                self.Meta.model.objects.get(cart=self.cleaned_data["cart"], product=self.cleaned_data["product"])
            except self.Meta.model.DoesNotExist:
                self.save()
            except self.Meta.model.MultipleObjectsReturned:
                self.Meta.model.objects.filter(cart=self.cleaned_data["cart"],
                                               product=self.cleaned_data["product"]).delete()
                self.save()
        elif self.cleaned_data["request_type"] == "del":
            try:
                self.Meta.model.objects.get(product=self.cleaned_data['product']).delete()
            except self.Meta.model.DoesNotExist:
                pass
            except self.Meta.model.MultipleObjectsReturned:
                self.Meta.model.objects.filter(cart=self.cleaned_data["cart"],
                                               product=self.cleaned_data["product"]).delete()


class DiscountForm(forms.Form):
    id = forms.UUIDField()
    cart_purchase_amount = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

    def clean_id(self):
        id = self.cleaned_data["id"]

        if not Discount.objects.filter(id=id).exists():
            print("nok")
            raise ValidationError("Discount is not valid")
        return id

    def get_discount(self):
        print(self.cleaned_data["id"])
        return Discount.objects.get(id=self.cleaned_data["id"]).discount_purchase_amount


class ReviewForm(forms.ModelForm):
    captcha = CaptchaField(
        widget=CustomCaptchaTextInput(attrs={'class': "form-control", 'aria-describedby': 'button-submit'}))

    class Meta:
        model = Review
        fields = ("name", "email", "title", "comment", "product", 'rate')
        widgets = {
            "product": forms.TextInput(attrs={'hidden': True}),
            "rate": forms.NumberInput(attrs={'hidden': True}),
            "comment": forms.Textarea(attrs={'class': 'form-control mb-0 mt-0'}),
            "name": forms.TextInput(attrs={'class': 'form-control mb-0 mt-0'}),
            "title": forms.TextInput(attrs={'class': 'form-control mb-0 mt-0'}),
            "email": forms.EmailInput(attrs={'class': 'form-control mb-0 mt-0'}),
        }

    def clean_rate(self):
        rate = self.cleaned_data['rate']
        rate *= 20
        return rate


class OrderForm(forms.ModelForm):
    cart = forms.ModelChoiceField(queryset=None, widget=forms.TextInput(attrs={'hidden': True}))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        self.fields["cart"].queryset = Cart.objects.filter(pk=self.request.cart.id)
        self.fields["address"].queryset = self.request.user.address_set.all()

    class Meta:
        model = Order
        fields = ("owner", "address", "shipping", "discount",)
        widgets = {
            "owner": forms.TextInput(attrs={'hidden': True}),
            "address": forms.TextInput(attrs={'hidden': True}),
            "shipping": forms.TextInput(attrs={'hidden': True}),
            "discount": forms.TextInput(attrs={'hidden': True}),
        }
