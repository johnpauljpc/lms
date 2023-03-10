from django.urls import path
from .views import index, singleCourse, contactUs, aboutUs

urlpatterns = [
    path('', index, name='home'),
    path('course/', singleCourse, name="courses"),
    path('contact-us/', contactUs, name="contact-us"),
    path('about-us/', aboutUs, name='about-us'),
]