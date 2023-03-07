from django.shortcuts import render
from .models import Categories

# Create your views here.
def index(request):
    categories = Categories.objects.all()
    context = {
        'categories':categories
    }
    return render(request, "lms/index.html", context)


def singleCourse(request):
    return render(request, "lms/single_course.html")

def contactUs(request):
    return render(request, 'lms/contact_us.html')


def aboutUs(request):
    return render(request, 'lms/about-us.html')