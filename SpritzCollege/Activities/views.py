from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Event, Course

# Create your views here.

class EventsList (ListView):
    title = "Events"
    model = Event
    template_name = "Activities/events.html"

class CoursesList (ListView):
    title = "Courses"
    model = Course
    template_name = "Activities/courses.html"