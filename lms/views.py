from django.shortcuts import render
from .models import Categories, Course
# Create your views here.

def index(request):
    categories = Categories.objects.all().order_by('-id')[:4]
    courses = Course.objects.filter(status = 'PUBLISH').order_by('-id')[:8]
    context = {
        'categories':categories,
        'courses':courses
    }
    
    return render(request, "lms/index.html", context)


def singleCourse(request):
    return render(request, "lms/single_course.html")

def contactUs(request):
    return render(request, 'lms/contact_us.html')


def aboutUs(request):
    return render(request, 'lms/about-us.html')