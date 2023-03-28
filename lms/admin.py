from django.contrib import admin
from .models import (Categories, Author, Course, Level,
                     things_you_wil_learn, Course_Requirements,
                     Lesson, Video, Language)

class things2learnInline(admin.TabularInline):
    model = things_you_wil_learn

class courseRequirementsInline(admin.TabularInline):
    model = Course_Requirements

class Lesson_Inline(admin.TabularInline):
    model = Lesson

class Video_Inline(admin.TabularInline):
    model = Video

class courseAdmin(admin.ModelAdmin):
    inlines = things2learnInline, courseRequirementsInline,  Video_Inline

# Register your models here.
admin.site.register(Categories)
admin.site.register(Author)
admin.site.register(Course, courseAdmin)
admin.site.register(Level)
admin.site.register(things_you_wil_learn)
admin.site.register(Course_Requirements)
admin.site.register(Lesson)
admin.site.register(Video)
admin.site.register(Language)