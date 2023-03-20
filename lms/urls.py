from django.urls import path
from .views import (index, Courses, contactUs, 
                    aboutUs,filter_data, searchField,courseDetail,
                    pageNotFound)

urlpatterns = [
    path('', index, name='home'),
    path('courses/', Courses, name="courses"),
    path('course/<slug:slug>/', courseDetail, name="course-detail"),

    path('filter-data/', filter_data, name='filter-data'),
    path('contact-us/', contactUs, name="contact-us"),
    path('about-us/', aboutUs, name='about-us'),
    path('search/', searchField, name='search'),
    path('not-found/', pageNotFound, name='404')
]