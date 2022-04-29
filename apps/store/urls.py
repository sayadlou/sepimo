from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('cart/', CartListAddView.as_view(), name='cart'),
    path('cart/<int:pk>', CartPutDeleteView.as_view(), name='cart_item'),
    path('orders/', OrderListView.as_view(), name='orders'),
    path('order/<uuid:pk>', OrderDetailView.as_view(), name='order_item'),
    path('payment/', PaymentListAddView.as_view(), name='payments'),

]
