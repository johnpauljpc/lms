from django.shortcuts import render
from .models import Categories, Course, Level
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
    categories = Categories.get_all_categories(Categories)
    level = Level.objects.all()
    courses = Course.objects.filter(status = 'PUBLISH').order_by('-id')
    
    context = {
        'categories':categories,
        'level':level,
        'courses':courses
        

    }
    print(f'LEVELS>>>>>>>> {level}')
    return render(request, "lms/single_course.html", context)

def contactUs(request):
    return render(request, 'lms/contact_us.html')


def aboutUs(request):
    return render(request, 'lms/about-us.html')