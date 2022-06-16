from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm, UsernameField, PasswordResetForm, PasswordChangeForm, \
    SetPasswordForm
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import UserProfile, Address
from .widget import CustomCaptchaTextInput


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ("owner", "province", "city", "phone_number", "area", "postal_code", "address",)
        required = ("owner",)
        widgets = {
            "owner": forms.TextInput(attrs={'hidden': True}),
            "province": forms.TextInput(attrs={'class': 'form-control mt-0 mb-0'}),
            "city": forms.TextInput(attrs={'class': 'form-control mt-0 mb-0'}),
            "phone_number": forms.TextInput(attrs={'class': 'form-control mt-0 mb-0'}),
            "area": forms.TextInput(attrs={'class': 'form-control mt-0 mb-0'}),
            "postal_code": forms.TextInput(attrs={'class': 'form-control mt-0 mb-0'}),
            "address": forms.Textarea(attrs={'class': 'form-control mt-0 mb-0', 'rows': 4}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'email', 'mobile', 'phone',)
        widgets = {
            'first_name': forms.TextInput(attrs={'autofocus': True, 'class': "form-control my-1"}),
            'last_name': forms.TextInput(attrs={'autofocus': True, 'class': "form-control  my-1"}),
            'mobile': forms.TextInput(attrs={'autofocus': True, 'class': "form-control  my-1"}),
            'phone': forms.TextInput(attrs={'autofocus': True, 'class': "form-control  my-1"}),
            'email': forms.EmailInput(attrs={'autofocus': True, 'class': "form-control  my-1"}),
        }


class MyAuthenticationForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class': "form-control"}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': "form-control"}),
    )
    captcha = CaptchaField(widget=CustomCaptchaTextInput(attrs={'class': "form-control"}))
    remember_me = forms.BooleanField(required=False)


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': "form-control"})
    )
    captcha = CaptchaField(widget=CustomCaptchaTextInput(attrs={'class': "form-control"}))


class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={'class': "form-control", 'autocomplete': 'current-password', 'autofocus': True}),
    )
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'class': "form-control", 'autocomplete': 'new-password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': "form-control", 'autocomplete': 'new-password'}),
    )


class MySetPasswordForm(SetPasswordForm):
    captcha = CaptchaField(widget=CustomCaptchaTextInput(attrs={'class': "form-control"}))
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'class': "form-control", 'autocomplete': 'new-password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': "form-control", 'autocomplete': 'new-password'}),
    )


class UserRegisterForm(UserCreationForm):
    captcha = CaptchaField(widget=CustomCaptchaTextInput(attrs={'class': "form-control"}))
    username = UsernameField(
        label=_("Username"),
        widget=forms.TextInput(attrs={'class': "form-control", 'autocomplete': 'off'})
    )

    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'class': "form-control", 'autocomplete': 'off'})
    )

    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': "form-control", 'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'class': "form-control", 'autocomplete': 'new-password'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password1', 'password2']
