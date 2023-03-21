from django.contrib import admin
from .models import (Categories, Author, Course, Level,
                     things_you_wil_learn, Course_Requirements)

# Register your models here.
admin.site.register(Categories)
admin.site.register(Author)
admin.site.register(Course)
admin.site.register(Level)
admin.site.register(things_you_wil_learn)
admin.site.register(Course_Requirements)