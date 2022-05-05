from django.urls import path

from .views import Blog,  Slug

urlpatterns = [
    path('', Blog.as_view(), name='home'),
    path('category/<str:category>', Blog.as_view(), name='category'),
    path('post/<str:slug>', Slug.as_view(), name='slug'),
]
