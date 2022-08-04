from captcha.fields import CaptchaField
from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.utils.translation import gettext as _

from .models import *
from .widget import CustomCaptchaTextInput


class CartItemEditForm(forms.ModelForm):
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

    def save(self, commit=True):
        return super().save(commit)

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


class CartItemAddForm(forms.ModelForm):
    request_type = forms.CharField(max_length=3, required=True)

    class Meta:
        model: CartItem = CartItem
        fields = ('cart', 'quantity', 'product', 'request_type')

    def save_or_add_existing(self):
        try:
            cart_item = self.Meta.model.objects.get(cart=self.instance.cart, product=self.instance.product)
            cart_item.quantity += self.instance.quantity
            cart_item.save()
        except CartItem.DoesNotExist:
            self.instance.save()
        except CartItem.MultipleObjectsReturned:
            cart_items_sum = CartItem.objects.filter(cart=self.cart, product=self.product).aggregate(Sum('quantity'))
            self.Meta.model.objects.filter(cart=self.cart, product=self.product).delete()
            self.instance.quantity += cart_items_sum["quantity__sum"]
            self.instance.save()


class ReviewForm(forms.ModelForm):
    captcha = CaptchaField(
        widget=CustomCaptchaTextInput(attrs={'class': "form-control", 'aria-describedby': 'button-submit'}))

    class Meta:
        model = Review
        fields = ("name", "email", "title", "comment", "product",)
        widgets = {
            "product": forms.TextInput(attrs={'hidden': True}),
            "comment": forms.Textarea(attrs={'class': 'form-control mb-0 mt-0'}),
            "name": forms.TextInput(attrs={'class': 'form-control mb-0 mt-0'}),
            "title": forms.TextInput(attrs={'class': 'form-control mb-0 mt-0'}),
            "email": forms.EmailInput(attrs={'class': 'form-control mb-0 mt-0'}),
        }
