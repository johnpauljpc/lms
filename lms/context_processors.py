from .models import Categories


def sitewide(request):
    return {
        'categories': Categories.objects.all().order_by('id'),
    }
