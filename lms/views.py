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
    categories = Categories.objects.all().order_by('-id')
    courses = Course.objects.filter(status = 'PUBLISH').order_by('-id')[:8]
    
    context = {
        'categories':categories,
        'courses':courses
    }
    
    return render(request, "lms/index.html", context)


def Courses(request):
    categories = Categories.get_all_categories(Categories)
    level = Level.objects.all()
    courses = Course.objects.filter(status = 'PUBLISH').order_by('-id')
    freeCourses = Course.objects.filter(price = 0).count()
    paidCourses = Course.objects.filter(price__gte = 1)
    print('paidCourses >>>>>>>>>>>>>>>>> ', paidCourses)
    
    context = {
        'categories':categories,
        'level':level,
        'courses':courses,
        'freeCourses':freeCourses,
        'paidCourses': paidCourses
        

    }
    
    return render(request, "lms/single_course.html", context)

def courseDetail(request, slug):
   course = Course.objects.filter(slug=slug)
   categories = Categories.get_all_categories(Categories)
   time_duration = Video.objects.filter(course__slug = slug).aggregate(sum = Sum('duration'))
   sum_of_author_courses = Course.objects.filter(slug = slug).count()  # sum_of_author_courses = Author.objects.filter(author = course.author).aggregate(sum = Sum())
   
   # check is user is enrolled
   course_id = Course.objects.get(slug=slug)
   if request.user.is_authenticated:
      try:
         Enrolled = UserCourse.objects.get(user = request.user, course = course_id)
      except UserCourse.DoesNotExist:
         Enrolled = None
   Enrolled = None

   if course.exists():
      course = course.first()
   else:
      return redirect('404')
   context = {
      'course':course,
      'categories':categories,
      'time_duration':time_duration,
      'sum_of_author_courses': sum_of_author_courses,
      'Enrolled':Enrolled
   }
   
   return render(request, 'lms/course-details.html', context)



def contactUs(request):
    categories = Categories.get_all_categories(Categories)
    context = {
       'categories':categories,
    }
    return render(request, 'lms/contact_us.html', context)


def aboutUs(request):
    categories = Categories.get_all_categories(Categories)
    context = {
       'categories':categories,
    }
    return render(request, 'lms/about-us.html', context)


def filter_data(request):
    categories = request.GET.getlist('category[]')
    level = request.GET.getlist('level[]')
    price = request.GET.getlist('price[]')
    print(f'LEVELS>>>>>>>> {level}')


    if price == ['priceFree']:
       course = Course.objects.filter(price=0)
      
    elif price == ['pricePaid']:
       course = Course.objects.filter(price__gte=1)
    elif price == ['priceAll']:
       course = Course.objects.all()
    elif categories:
       course = Course.objects.filter(category__id__in=categories).order_by('-id')
    elif level:
       course = Course.objects.filter(level__id__in = level).order_by('-id')
    else:
       course = Course.objects.all().order_by('-id')

    number_courses = course.count()
    print (">>>>>>>>>>>>>>   ", number_courses)
    t = render_to_string('ajax/course.html', context = {'course': course, 'number_courses':number_courses})

    return JsonResponse({'data': t})
   

def searchField(request):
   q = request.GET['search-query']
   categories = Categories.get_all_categories(Categories)
   
   courses = Course.objects.filter(Q(title__icontains=q)|Q(description__icontains=q) | Q(category__name__icontains=q))
   print('>>>>>>>>>>>>>>>>>>>>> SS  ', courses)
   context = {'query': q, 'courses':courses, 'categories':categories}
   return render(request, 'search/search.html', context=context)
#  return redirect(request.META.get("HTTP_REFERER", "/")

def pageNotFound(request):
   categories = Categories.get_all_categories(Categories)
   context = {
       'categories':categories,
    }
   return render(request, 'error/404.html', context)


@login_required(login_url='login')
def CheckoutView(request, slug):
   course = Course.objects.get(slug=slug)

   if course.price == 0:
      usercourse = UserCourse(
         user = request.user,
         course = course
      )
      usercourse.save()
      messages.success(request, f"<b>{course}</b> successfully enrolled")
      return redirect('home')
   
   course_id = Course.objects.get(slug = slug)
   try:
      enroll_status = UserCourse.objects.get(user = request.user, course = course_id)
   except UserCourse.DoesNotExist:
      enroll_status = None
   return render(request, 'lms/checkout.html')


   
# def CheckoutView(request, slug):
#       return render(request, 'lms/checkout.html')

class MyCourses(View):
   
   def get(self, request):
      course = UserCourse.objects.filter(user__id = request.user.id)
      context = {
         'courses':course
      }
      
      return render (request, 'lms/my-courses.html', context=context)
   
   def post(self, request):
      return render (request, 'lms/my-courses.html')

def Watch_Course(request, slug):
   # lecture = request.GET.get('lecture')
   # print('>>>>>>>>>>>>>>>>>>>>                ', lecture)
   course_id = Course.objects.get(slug = slug)
   course = Course.objects.filter(slug = slug)

   try:
      check_enroll  = UserCourse.objects.get(user = request.user, course = course_id)
      # video = Video.objects.get(id = lecture)

      if course.exists():
         course = course.first()
      else:
         return redirect('404')
   except UserCourse.DoesNotExist:
      return redirect('404')
   

   context = {
      # 'lecture': lecture,
      'course': course,
      # 'video': video
   }
   print(context)
   
   
   return render(request, 'course/watch-course.html', context)