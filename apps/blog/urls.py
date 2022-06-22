from django.urls import path

from .views import Blog, Slug, CommentCreateFormView, CommentCreateSuccessView

urlpatterns = [
    path('', Blog.as_view(), name='home'),
    path('category/<str:category>', Blog.as_view(), name='category'),
    path('post/<str:slug>', Slug.as_view(), name='slug'),
    path('comment_form/', CommentCreateFormView.as_view(), name='comment_form'),
    path('comment_made/', CommentCreateSuccessView.as_view(), name='comment_made'),
]
