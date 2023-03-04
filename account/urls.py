from django.urls import path

from .views import loginView, registrationView, logoutView

urlpatterns = [
    path('login/', loginView, name='login' ),
    path('register/', registrationView, name= 'register'),
    path('logout/', logoutView, name = 'logout'),
]