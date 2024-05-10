from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Event, Course

# Create your views here.

class EventsList (ListView):
    model = Event
    template_name = "Activities/events.html"
    
    def get_context_data(self, **kwargs):
        context = super(EventsList, self).get_context_data(**kwargs)
        context['title'] = "Events"
        return context

class CoursesList(ListView):
    model = Course
    template_name = "Activities/courses.html"
    
    def get_context_data(self, **kwargs):
        context = super(CoursesList, self).get_context_data(**kwargs)
        context['title'] = "Courses"
        return context
