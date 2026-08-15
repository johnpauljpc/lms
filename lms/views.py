from django.shortcuts import render, redirect
from .models import (Categories, Course, Level, Video,
                     Author, UserCourse)

from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Q, Sum
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


def index(request):
    courses = Course.objects.filter(status='PUBLISH').order_by('-id')[:8]
    context = {
        'courses': courses
    }
    return render(request, "lms/index.html", context)


def Courses(request):
    level = Level.objects.all()
    courses = Course.objects.filter(status='PUBLISH').order_by('-id')
    freeCourses = Course.objects.filter(status='PUBLISH', price=0).count()
    paidCourses = Course.objects.filter(status='PUBLISH', price__gte=1)

    context = {
        'level': level,
        'courses': courses,
        'freeCourses': freeCourses,
        'paidCourses': paidCourses,
        'number_courses': courses.count(),
    }

    return render(request, "lms/single_course.html", context)


def courseDetail(request, slug):
    course = Course.objects.filter(slug=slug, status='PUBLISH')
    if not course.exists():
        return redirect('404')
    course = course.first()

    time_duration = Video.objects.filter(course=course).aggregate(sum=Sum('duration'))
    sum_of_author_courses = Course.objects.filter(author=course.author, status='PUBLISH').count()

    # check is user is enrolled
    if request.user.is_authenticated:
        try:
            Enrolled = UserCourse.objects.get(user=request.user, course=course)
        except UserCourse.DoesNotExist:
            Enrolled = None
    else:
        Enrolled = None

    context = {
        'course': course,
        'time_duration': time_duration,
        'sum_of_author_courses': sum_of_author_courses,
        'Enrolled': Enrolled,
    }

    return render(request, 'lms/course-details.html', context)


def contactUs(request):
    return render(request, 'lms/contact_us.html')


def aboutUs(request):
    return render(request, 'lms/about-us.html')


def filter_data(request):
    categories = request.GET.getlist('category[]')
    level = request.GET.getlist('level[]')
    price = request.GET.getlist('price[]')

    courses = Course.objects.filter(status='PUBLISH')

    if price and price != ['priceAll']:
        if 'priceFree' in price:
            courses = courses.filter(price=0)
        if 'pricePaid' in price:
            courses = courses.filter(price__gte=1)
        if not {'priceFree', 'pricePaid'} & set(price):
            courses = courses.filter(price__gte=0)

    if categories:
        courses = courses.filter(category__id__in=categories)
    if level:
        courses = courses.filter(level__id__in=level)

    courses = courses.order_by('-id')
    number_courses = courses.count()
    t = render_to_string('ajax/course.html', context={'course': courses, 'number_courses': number_courses})

    return JsonResponse({'data': t})


def searchField(request):
    q = request.GET.get('search-query', '').strip()
    courses = Course.objects.filter(status='PUBLISH').filter(
        Q(title__icontains=q) | Q(description__icontains=q) | Q(category__name__icontains=q)
    )
    context = {'query': q, 'courses': courses}
    return render(request, 'search/search.html', context=context)


def pageNotFound(request):
    return render(request, 'error/404.html')


@login_required(login_url='login')
def CheckoutView(request, slug):
    try:
        course = Course.objects.get(slug=slug)
    except Course.DoesNotExist:
        return redirect('404')

    if course.price == 0:
        _, created = UserCourse.objects.get_or_create(user=request.user, course=course)
        if created:
            messages.success(request, f"<b>{course}</b> successfully enrolled")
        else:
            messages.info(request, f"You have already enrolled on <b>{course.title}</b>!")
        return redirect('my-courses')

    if UserCourse.objects.filter(user=request.user, course=course).exists():
        messages.info(request, f"You have enrolled on <b>{course.title}</b> already!")
        return redirect('my-courses')

    context = {
        'course': course,
    }
    return render(request, 'lms/checkout.html', context)


class MyCourses(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        courses = UserCourse.objects.filter(user=request.user).select_related('course', 'course__author', 'course__category')
        context = {
            'courses': courses
        }
        return render(request, 'lms/my-courses.html', context=context)


@login_required(login_url='login')
def Watch_Course(request, slug):
    try:
        course = Course.objects.get(slug=slug)
    except Course.DoesNotExist:
        return redirect('404')

    if not UserCourse.objects.filter(user=request.user, course=course).exists():
        return redirect('404')

    lecture = request.GET.get('lecture')
    video = Video.objects.filter(id=lecture, course=course).first()
    if video is None:
        video = Video.objects.filter(course=course).order_by('serial_number', 'id').first()

    context = {
        'course': course,
        'video': video,
    }

    return render(request, 'course/watch-course.html', context)