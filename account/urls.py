from django.urls import path

from .views import (loginView, registrationView, logoutView, resetPasswordDone,
                    resetPassword, passwordResetConfirmation, profile)
from django.contrib.auth.views import (PasswordResetView, PasswordResetConfirmView,
                                       PasswordResetDoneView, PasswordResetCompleteView)


urlpatterns = [
    path('login/', loginView, name='login' ),
    path('register/', registrationView, name= 'register'),
    path('logout/', logoutView, name = 'logout'),

    # PASSWORD RESETTING
    path('reset-password/', resetPassword, name='reset-password' ),
    path('reset-password-done/', resetPasswordDone, name='reset-password-done' ),
    path('reset/<uidb64>/<token>/', passwordResetConfirmation, name="reset-confirm"),

    path('profile/', profile, name="profile"),
    
    
    
]