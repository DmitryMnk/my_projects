from django.contrib import admin
from .models import *


admin.site.register(CourseLevel)
admin.site.register(CourseCategory)
admin.site.register(CourseSubCategory)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = 'pk', 'name', 'category', 'level'
    list_display_links = 'pk', 'name', 'category', 'level'
    ordering = 'pk', 'name', 'category'
