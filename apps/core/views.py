from django.views.generic import TemplateView

from apps.core.models import AboutUsPage, CustomerReviews, HomePage
from apps.store.models import Brand


class Home(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = HomePage.get_data()
        context['title'] = HomePage.get_data().title
        return context


class AboutUs(TemplateView):
    template_name = 'core/about_us.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = AboutUsPage.get_data()
        context['title'] = AboutUsPage.get_data().title
        context['brands'] = Brand.objects.all()
        context['reviews'] = CustomerReviews.objects.all()
        return context
