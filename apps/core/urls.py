from django.urls import path
from django.views.generic import TemplateView

from .views import Home, AboutUs, Menu

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('about_us/', AboutUs.as_view(), name='about_us'),
    path('menu/', Menu.as_view(), name='menu'),

]
