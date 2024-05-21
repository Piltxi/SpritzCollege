from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Event, Course
from braces.views import GroupRequiredMixin
from django.views.generic.edit import CreateView
from .forms import *
from django.contrib.auth.decorators import login_required

# Create your views here.

class AddEvents (GroupRequiredMixin, CreateView):
    group_required = ["culture"]
    # title = "Aggiungi un libro alla biblioteca"
    form_class = EventForm
    template_name = "control_panel.html"
    success_url = reverse_lazy("home")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "New Event"
        return context

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

class EventDetail (DetailView):
    model = Event
    template_name = 'Activities/event_detail.html'

def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'Activities/course_detail.html', {'course': course})

@login_required
def book_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.event = event
            try:
                booking.clean()  # Validazioni personalizzate
                booking.save()
                return redirect('event_detail', event_id=event.id)
            except ValidationError as e:
                form.add_error(None, e)
    else:
        form = BookingForm()
    return render(request, 'Activities/book_event.html', {'form': form, 'event': event})

class EventDeleteView(DeleteView):
    model = Event
    success_url = reverse_lazy('event_list')  # L'URL a cui reindirizzare dopo l'eliminazione
