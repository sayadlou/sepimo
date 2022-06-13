from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView, DetailView

from .forms import MyAuthenticationForm, MyPasswordResetForm, MyPasswordChangeForm, MySetPasswordForm, UserRegisterForm, \
    ProfileForm, AddressForm
from .models import UserProfile, Address
from ..core.models import LoginPage, SignUpPage, ProfilePage


class Login(LoginView):
    form_class = MyAuthenticationForm
    template_name = 'account/login.html'

    def get_success_url(self):
        url = self.request.POST.get('next', "")
        if url == "":
            return reverse("account:profile")
        return url

    def form_valid(self, form):
        remember_me = form.cleaned_data['remember_me']  # get remember me data from cleaned_data of form
        if not remember_me:
            self.request.session.set_expiry(0)  # if remember me is
            self.request.session.modified = True
        return super(Login, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["page"] = LoginPage.get_data()
        context["title"] = LoginPage.get_data().title
        return context


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["page"] = SignUpPage.get_data()
        context["title"] = SignUpPage.get_data().title
        return context


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
        data["page"] = ProfilePage.get_data()
        data["title"] = ProfilePage.get_data().title
        data["orders"] = self.request.user.Orders.all()
        data["addresses"] = Address.objects.filter(owner=self.request.user)
        data['new_address_form'] = AddressForm({'owner': self.request.user})
        return data


class AddressViewList(LoginRequiredMixin, ListView):
    template_name = 'account/address_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['addresses'] = self.object_list
        return context

    def get_queryset(self):
        return Address.objects.filter(owner=self.request.user)


class AddressView(LoginRequiredMixin, UpdateView):
    template_name = 'account'

    def get_object(self, queryset=None):
        return Address.objects.filter(owner=self.request.user, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context


class AddressViewCreate(LoginRequiredMixin, CreateView):
    template_name = 'account/new_address_form.html'
    form_class = AddressForm

    def get_success_url(self):
        return reverse('account:list-address')

    def get_initial(self):
        return {"owner": self.request.user}
