from django.urls import path

from .views import loginView, registrationView

urlpatterns = [
    path('login/', loginView, name='login' ),
    path('register/', registrationView, name= 'register'),
]