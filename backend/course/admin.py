from django.contrib import admin

from .models import Certificate, Course, Lesson, LessonProgress, Module, UserCourse

admin.site.register(Course)
admin.site.register(Certificate)
admin.site.register(UserCourse)
admin.site.register(LessonProgress)

class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')

admin.site.register(Lesson, LessonAdmin)
admin.site.register(Module)
