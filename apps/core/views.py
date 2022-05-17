from django.views.generic import TemplateView

from apps.core.models import AboutUsPage, Brand, CustomerReviews


class Home(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AboutUs(TemplateView):
    template_name = 'core/about_us.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = AboutUsPage.get_setting()
        context['title'] = AboutUsPage.get_setting().title
        context['brands'] = Brand.objects.all()
        context['reviews'] = CustomerReviews.objects.all()
        return context
