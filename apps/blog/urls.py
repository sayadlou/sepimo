from django.urls import path

from .views import BlogView, Slug ,CategoryView

urlpatterns = [
    path('', BlogView.as_view(), name='home'),
    path('category/<str:category>', CategoryView.as_view(), name='category'),
    path('post/<str:slug>', Slug.as_view(), name='slug'),

]
