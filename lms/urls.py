from django.urls import path
from .views import index, singleCourse, contactUs, aboutUs,filter_data

urlpatterns = [
    path('', index, name='home'),
    path('course/', singleCourse, name="courses"),
    path('product/filter-data', filter_data, name='filter-data'),
    path('contact-us/', contactUs, name="contact-us"),
    path('about-us/', aboutUs, name='about-us'),
    
]