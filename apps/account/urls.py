from django.urls import path

from .views import *

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('profile/', Profile.as_view(), name='profile'),
    path('profile/update/', ProfileUpdateView.as_view(), name='update-profile'),
    path('profile/addresses/', AddressListView.as_view(), name='list-address'),
    path('profile/address/create/', AddressViewCreate.as_view(), name='create-address'),
    path('profile/address/<uuid:pk>/update/', AddressUpdateView.as_view(), name='edit-address'),
    path('profile/address/<uuid:pk>/delete/', AddressDeleteView.as_view(), name='delete-address'),

    path('password_change/', PasswordChange.as_view(), name='password_change'),
    path('password_change/done/', PasswordChangeDone.as_view(), name='password_change_done'),

    path('password_reset/', PasswordReset.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDone.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetComplete.as_view(), name='password_reset_complete'),

]
