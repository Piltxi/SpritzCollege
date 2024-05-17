from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Event, Course
from braces.views import GroupRequiredMixin
from django.views.generic.edit import CreateView
from .forms import *

# Create your views here.

class AddEvents (GroupRequiredMixin, CreateView):
    group_required = ["culture"]
    title = "Aggiungi un libro alla biblioteca"
    form_class = EventForm
    template_name = "Activities/add.html"
    success_url = reverse_lazy("home")

class EventsList (ListView):
    model = Event
    template_name = "Activities/events.html"
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_string = self.request.GET.get("search_string", "")
        search_where = self.request.GET.get("search_where", "")

        # Debugging prints
        print(f"Search String: {search_string}")  
        print(f"Search Where: {search_where}")

        if search_string and search_where:
            if search_where == "Name":
                queryset = queryset.filter(name__icontains=search_string)
            elif search_where == "Description":
                queryset = queryset.filter(description__icontains=search_string)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(EventsList, self).get_context_data(**kwargs)
        form = SearchForm (self.request.GET or None)
        context["form"] = form
        context['title'] = "Events"
        return context

class CoursesList(ListView):
    model = Course
    template_name = "Activities/courses.html"
    
    def get_context_data(self, **kwargs):
        context = super(CoursesList, self).get_context_data(**kwargs)
        context['title'] = "Courses"
        return context

def event_detail(request, event_id):
    event = get_object_or_404 (Event, pk=event_id)
    return render(request, 'Activities/event_detail.html', {'event': event})

def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'Activities/course_detail.html', {'course': course})