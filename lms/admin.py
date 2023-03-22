from django.contrib import admin
from .models import (Categories, Author, Course, Level,
                     things_you_wil_learn, Course_Requirements)

class things2learnInline(admin.TabularInline):
    model = things_you_wil_learn

class courseRequirementsInline(admin.TabularInline):
    model = Course_Requirements

class courseAdmin(admin.ModelAdmin):
    inlines = things2learnInline, courseRequirementsInline

# Register your models here.
admin.site.register(Categories)
admin.site.register(Author)
admin.site.register(Course, courseAdmin)
admin.site.register(Level)
admin.site.register(things_you_wil_learn)
admin.site.register(Course_Requirements)