from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "lms/index.html")


def singleCourse(request):
    return render(request, "lms/single_course.html")

def contactUs(request):
    return render(request, 'lms/contact_us.html')


def aboutUs(request):
    return render(request, 'lms/about-us.html')