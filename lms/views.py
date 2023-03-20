from django.shortcuts import render, redirect
from .models import Categories, Course, Level

from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Q

# Create your views here.

def index(request):
    categories = Categories.objects.all().order_by('-id')[:4]
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

   if course.exists():
      course = course.first()
   else:
      return redirect('404')
   context = {
      'course':course
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
   courses = Course.objects.filter(Q(title__icontains=q)|Q(description__icontains=q) | Q(category__name__icontains=q))
   print('>>>>>>>>>>>>>>>>>>>>> SS  ', courses)
   context = {'query': q, 'courses':courses}
   return render(request, 'search/search.html', context=context)
#  return redirect(request.META.get("HTTP_REFERER", "/")

def pageNotFound(request):
   return render(request, 'error/404.html')