from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import MyAuthenticationForm, MyPasswordResetForm, MyPasswordChangeForm, MySetPasswordForm, UserRegisterForm, \
    ProfileForm
from .models import UserProfile


class Login(LoginView):
    form_class = MyAuthenticationForm
    template_name = 'account/login.html'

    def form_valid(self, form):
        remember_me = form.cleaned_data['remember_me']  # get remember me data from cleaned_data of form
        if not remember_me:
            self.request.session.set_expiry(0)  # if remember me is
            self.request.session.modified = True
        return super(Login, self).form_valid(form)


class Logout(LogoutView):
    template_name = 'account/logged_out.html'
    next_page = reverse_lazy('core:home')


class PasswordChange(PasswordChangeView):
    success_url = reverse_lazy('account:password_change_done')
    template_name = 'account/password_change_form.html'
    form_class = MyPasswordChangeForm


class PasswordChangeDone(PasswordChangeDoneView):
    template_name = 'account/password_change_done.html'


class PasswordReset(PasswordResetView):
    subject_template_name = 'account/password_reset_subject.txt'
    email_template_name = 'account/password_reset_email.html'
    template_name = 'account/password_reset_form.html'
    success_url = reverse_lazy('account:password_reset_done')
    form_class = MyPasswordResetForm


class PasswordResetDone(PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    success_url = reverse_lazy('account:password_reset_complete')
    template_name = 'account/password_reset_confirm.html'
    form_class = MySetPasswordForm


class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'


class SignUp(CreateView):
    template_name = 'account/signup.html'
    model = UserProfile
    form_class = UserRegisterForm

    def get_success_url(self):
        return reverse_lazy('account:profile')


class Profile(LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    login_url = reverse_lazy('account:login')

    template_name = "account/profile.html"
    context_object_name = "obj"

    def get_success_url(self):
        return reverse_lazy('account:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        data = super().get_context_data()
        data["saeid"] = "asawdawdawdqwdqwd"
        # user_purchased_base_product = self.request.user.productbasemodel_set.all()
        # user_purchased_product = set()
        # for base_product in user_purchased_base_product:
        #     user_purchased_product.add(base_product.get_child())
        # data["purchase"] = user_purchased_product
        return data
