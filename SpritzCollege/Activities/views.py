from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Event, Course, Booking
from braces.views import GroupRequiredMixin
from .forms import BookingForm, EventForm, SearchForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

# Create your views here.

class AddEvents(GroupRequiredMixin, CreateView):
    group_required = ["culture"]
    form_class = EventForm
    template_name = "control_panel.html"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "New Event"
        return context

class EventsList(ListView):
    model = Event
    template_name = "Activities/events.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        search_string = self.request.GET.get("search_string", "")
        search_where = self.request.GET.get("search_where", "")

        if search_string and search_where:
            if search_where == "Name":
                queryset = queryset.filter(name__icontains=search_string)
            elif search_where == "Description":
                queryset = queryset.filter(description__icontains=search_string)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(EventsList, self).get_context_data(**kwargs)
        form = SearchForm(self.request.GET or None)
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
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'Activities/event_detail.html', {'event': event})

class EventDetail(DetailView):
    model = Event
    template_name = 'Activities/event_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['available_seats'] = self.object.available_seats
        return context

def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'Activities/course_detail.html', {'course': course})

# Prenotazione dell'evento
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
                return redirect('event_detail', pk=event.id)
            except ValidationError as e:
                form.add_error(None, e)
    else:
        form = BookingForm()
    return render(request, 'Activities/book_event.html', {'form': form, 'event': event})

@method_decorator(login_required, name='dispatch')
class EventDeleteView(DeleteView):
    model = Event
    success_url = reverse_lazy('list_events')
    template_name = 'Activities/event_detail.html'

    def get_queryset(self):
        # Assicurati che l'utente possa solo cancellare eventi che ha creato
        return super().get_queryset().filter(created_by=self.request.user)

@method_decorator(login_required, name='dispatch')
class MyBookingsListView(ListView):
    model = Booking
    template_name = "Activities/my_bookings.html"
    context_object_name = 'bookings'

    def get_queryset(self):
        # Assicurati che l'utente possa solo vedere le sue prenotazioni
        return Booking.objects.filter(user=self.request.user, event__status='active')

@method_decorator(login_required, name='dispatch')
class BookingDeleteView(DeleteView):
    model = Booking
    success_url = reverse_lazy('my_bookings')

    def get_queryset(self):
        # Assicurati che l'utente possa solo cancellare le sue prenotazioni
        return super().get_queryset().filter(user=self.request.user)

@method_decorator(login_required, name='dispatch')
class BookingUpdateView(UpdateView):
    model = Booking
    form_class = BookingForm
    template_name = 'Activities/booking_update.html'  # Template per la modifica della prenotazione
    success_url = '/'  # URL di reindirizzamento dopo il successo della modifica

    def get_queryset(self):
        # Assicurati che l'utente possa solo aggiornare le sue prenotazioni
        return super().get_queryset().filter(user=self.request.user)

class CultureGroupRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='culture').exists()
class PrenotazioniEventoView(LoginRequiredMixin, CultureGroupRequiredMixin, DetailView):
    model = Event
    template_name = 'Activities/prenotazioni_evento.html'
    context_object_name = 'evento'
    pk_url_kwarg = 'evento_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['prenotazioni'] = Booking.objects.filter(event=self.object)
        return context