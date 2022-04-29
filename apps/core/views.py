from django.shortcuts import render

from django.views.generic import TemplateView


class Home(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AboutUs(TemplateView):
    template_name = 'core/about_us.html'

    def get_context_data(self, **kwargs):
        pass
