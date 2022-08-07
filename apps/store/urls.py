from django.urls import path

from .views import *

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart-widget/', CartWidgetView.as_view(), name='cart-widget'),
    path('wishlist/', WishList.as_view(), name='whishlist'),
    path('discount/', DiscountView.as_view(), name='discount'),
    path('order/', OrderView.as_view(), name='order'),
    path('product/<str:pk>/', ProductView.as_view(), name='product-code'),
    path('product/<str:pk>/<str:slug>/', ProductView.as_view(), name='product-code-slug'),
]
