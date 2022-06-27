from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('products', ProductsView.as_view(), name='product'),
    path('product/<str:code>/<str:slug>', ProductView.as_view(), name='product'),
    path('orders/', OrderListView.as_view(), name='orders'),
    path('order/<uuid:pk>', OrderDetailView.as_view(), name='order_item'),
    path('payment/', PaymentListAddView.as_view(), name='payments'),
]
