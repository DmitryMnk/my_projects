from django.shortcuts import render
from django.views.generic import TemplateView

from courses.models import CourseCategory


class MainView(TemplateView):
    template_name = 'main/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'course_cats': CourseCategory.objects.all()
        })
        return context
