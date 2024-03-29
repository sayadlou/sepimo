from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, TemplateView

from .forms import MyAuthenticationForm, MyPasswordResetForm, MyPasswordChangeForm, MySetPasswordForm, UserRegisterForm, \
    AddressForm, ProfileForm
from .models import UserProfile, Address
from ..core.models import ProfilePage, PasswordResetPage, SignPage


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
        context["page"] = SignPage.get_data()
        context["title"] = SignPage.get_data().title
        return context


class Logout(LogoutView):
    template_name = 'account/logged_out.html'
    next_page = reverse_lazy('core:home')


class PasswordChange(PasswordChangeView):
    success_url = reverse_lazy('account:password_change_done')
    template_name = 'account/password_change_form.html'
    form_class = MyPasswordChangeForm

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['password_change_form'] = data.get('form')
        return data


class PasswordChangeDone(PasswordChangeDoneView):
    template_name = 'account/password_change_done.html'


class PasswordReset(PasswordResetView):
    subject_template_name = 'account/password_reset_subject.txt'
    email_template_name = 'account/password_reset_email.html'
    template_name = 'account/password_reset_form.html'
    success_url = reverse_lazy('account:password_reset_done')
    form_class = MyPasswordResetForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["page"] = PasswordResetPage.get_data()
        context["title"] = PasswordResetPage.get_data().title
        return context


class PasswordResetDone(PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["page"] = PasswordResetPage.get_data()
        context["title"] = PasswordResetPage.get_data().title
        return context


class PasswordResetConfirm(PasswordResetConfirmView):
    success_url = reverse_lazy('account:password_reset_complete')
    template_name = 'account/password_reset_confirm.html'
    form_class = MySetPasswordForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["page"] = PasswordResetPage.get_data()
        context["title"] = PasswordResetPage.get_data().title
        return context


class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["page"] = PasswordResetPage.get_data()
        context["title"] = PasswordResetPage.get_data().title
        return context


class SignUp(CreateView):
    template_name = 'account/signup.html'
    model = UserProfile
    form_class = UserRegisterForm

    def form_valid(self, form):
        redirect = super().form_valid(form)
        new_user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password1'],
                                )
        login(self.request, new_user)
        return redirect

    def get_success_url(self):
        return reverse_lazy('account:profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["page"] = SignPage.get_data()
        context["title"] = SignPage.get_data().title
        return context


class Profile(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('account:login')
    template_name = "account/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["page"] = ProfilePage.get_data()
        context["form"] = ProfileForm(instance=self.request.user)
        context["title"] = ProfilePage.get_data().title
        context["orders"] = self.request.user.Orders.all()
        context["addresses"] = Address.objects.filter(owner=self.request.user)
        context['new_address_form'] = AddressForm({'owner': self.request.user})
        context['password_change_form'] = MyPasswordChangeForm(user=self.request.user)

        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'account/edit_profile_form.html'
    form_class = ProfileForm

    def get_object(self, queryset=None):
        return UserProfile.objects.filter(pk=self.request.user.pk).first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context

    def get_success_url(self):
        return reverse('account:update-profile')


class AddressListView(LoginRequiredMixin, ListView):
    template_name = 'account/address_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['addresses'] = self.object_list
        return context

    def get_queryset(self):
        return Address.objects.filter(owner=self.request.user)


class AddressUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'account/edit_address_form.html'
    form_class = AddressForm

    def get_object(self, queryset=None):
        return Address.objects.filter(owner=self.request.user, pk=self.kwargs['pk']).first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context

    def get_success_url(self):
        return reverse('account:list-address')


class AddressDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'account/delete_address_form.html'

    def get_object(self, queryset=None):
        return Address.objects.filter(owner=self.request.user, pk=self.kwargs['pk']).first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context

    def get_success_url(self):
        return reverse('account:list-address')


class AddressViewCreate(LoginRequiredMixin, CreateView):
    template_name = 'account/new_address_form.html'
    form_class = AddressForm

    def get_success_url(self):
        return reverse('account:list-address')

    def get_initial(self):
        return {"owner": self.request.user}
