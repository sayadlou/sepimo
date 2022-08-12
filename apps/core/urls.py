from django.urls import path
from django.views.generic import TemplateView

from .views import Home, AboutUs

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('about_us/', AboutUs.as_view(), name='about_us'),
]
