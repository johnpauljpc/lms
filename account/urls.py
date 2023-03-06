from django.urls import path

from .views import loginView, registrationView, logoutView
from django.contrib.auth.views import (PasswordResetView, PasswordResetConfirmView,
                                       PasswordResetDoneView, PasswordResetCompleteView)


urlpatterns = [
    path('login/', loginView, name='login' ),
    path('register/', registrationView, name= 'register'),
    path('logout/', logoutView, name = 'logout'),
    
    # password reset

path('password-reset/', PasswordResetView.as_view(template_name='accounts/password_reset_form.html'), name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
]