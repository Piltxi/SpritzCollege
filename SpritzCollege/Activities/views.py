from datetime import timedelta
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Event, Course, Booking
from braces.views import GroupRequiredMixin
from django.contrib import messages
from .forms import BookingForm, EventForm, SearchForm, CourseForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

# Create your views here.

class CultureGroupRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='culture').exists()

class AddEvents(GroupRequiredMixin, CreateView):
    group_required = ["culture"]
    form_class = EventForm
    template_name = "Activities/new_activity.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        response = super().form_valid(form)
        print("Evento creato correttamente")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "New Event"
        return context
    
class AddCourse (GroupRequiredMixin, CreateView):
    group_required = ["culture"]
    form_class = CourseForm
    template_name = "Activities/new_activity.html"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "New Course"
        return context

class EventsList(ListView):
    model = Event
    template_name = "Activities/Events/events.html"

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
    template_name = "Activities/Courses/courses.html"

    def get_context_data(self, **kwargs):
        context = super(CoursesList, self).get_context_data(**kwargs)
        context['title'] = "Courses"
        return context

class EventDetail(DetailView):
    model = Event
    template_name = 'Activities/Events/event_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['available_seats'] = self.object.available_seats
        return context

class CourseDetail(DetailView):
    model = Course
    template_name = 'Activities/Courses/course_detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Puoi aggiungere altri dati al contesto se necessario
        return context

class EventUpdateView(CultureGroupRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'Activities/new_activity.html'
    success_url = reverse_lazy('list_events')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f' {self.get_object().name} \u2192 Update Event'
        return context

class CourseUpdateView(CultureGroupRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'Activities/new_activity.html'
    success_url = reverse_lazy('list_courses')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Course'
        return context

class EventDeleteView(CultureGroupRequiredMixin, DeleteView):
    model = Event
    success_url = reverse_lazy('list_events')
    template_name = 'Activities/event_detail.html'

class CourseDeleteView(CultureGroupRequiredMixin, DeleteView):
    model = Course
    success_url = reverse_lazy('list_courses')
    template_name = 'Activities/course_detail.html'

# deprecated _____________________________________________
def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'Activities/event_detail.html', {'event': event})

def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'Activities/course_detail.html', {'course': course})
# ________________________________________________________

@login_required
def book_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = BookingForm(request.POST, initial={'event': event})
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.event = event
            try:
                booking.clean() 
                booking.save()
                return redirect('event_detail', pk=event.id)
            except ValidationError as e:
                form.add_error(None, e)
        else: 
            errors = form.errors.as_json()
            return JsonResponse({'errors': errors}, status=400)
    else:
        form = BookingForm(initial={'event': event})
    return render(request, 'Activities/new_activity.html', {'title': f'{event.name} \u2192 Book Event', 'form': form, 'event': event})

@method_decorator(login_required, name='dispatch')
class MyBookingsListView(ListView):
    model = Booking
    template_name = "Activities/mybookings_event.html"
    context_object_name = 'bookings'

@method_decorator(login_required, name='dispatch')
class MyBookingDeleteView(DeleteView):
    model = Booking
    success_url = reverse_lazy('mybookings_events_view')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user != request.user:
            return redirect('mybookings_events_view')
        return super().delete(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class MyBookingUpdateView(UpdateView):
    model = Booking
    form_class = BookingForm
    template_name = 'Activities/booking_update.html'
    success_url = reverse_lazy('mybookings_events_view')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def form_valid(self, form):
        if self.get_object().user != self.request.user:
            return redirect('mybookings_events_view')
        return super().form_valid(form)
    
@method_decorator(login_required, name='dispatch')
class AdminBookingDeleteView(CultureGroupRequiredMixin, DeleteView):
    model = Booking
    success_url = reverse_lazy('prenotazioni_evento')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Prenotazione eliminata con successo!")
        return super().delete(request, *args, **kwargs)
    
@method_decorator(login_required, name='dispatch')
class AdminBookingUpdateView(CultureGroupRequiredMixin, UpdateView):
    model = Booking
    form_class = BookingForm
    template_name = 'Activities/booking_update.html'
    success_url = reverse_lazy('prenotazioni_evento')

    def get_success_url(self):
        event_id = self.object.event.id
        return reverse_lazy('prenotazioni_evento', kwargs={'evento_id': event_id})

# calendar ________________________________________________________
def generate_recurrence_dates(course):
    recurrence_dates = []
    current_date = course.start_date
    while current_date <= course.end_date:
        if current_date.strftime('%A').lower() == course.recurrence_day.lower():
            recurrence_dates.append(current_date)
        current_date += timedelta(days=1)
    return recurrence_dates

def calendar_view(request):
    events = Event.objects.all()
    courses = Course.objects.all()
    calendar_data = []

    for event in events:
        calendar_data.append({
            'id': event.id,
            'title': event.name,
            'start': event.date.isoformat(),
            'description': event.description,
            'type': 'event'
        })

    for course in courses:
        recurrence_dates = generate_recurrence_dates(course)
        for date in recurrence_dates:
            calendar_data.append({
                'id': course.id,
                'title': course.name,
                'start': date.isoformat(),
                'description': course.description,
                'type': 'course'
            })

    context = {
        'title': 'Calendar',
        'calendar_data': calendar_data
    }
    return render(request, 'Activities/calendar.html', context)
# calendar ________________________________________________________

# BOOKING USER VIEWS ______________________________________________
class UserBookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'Activities/event_bookings.html'
    
    def get_queryset(self):
        queryset = Booking.objects.filter(user=self.request.user).order_by('event__date')
        # print(f"Number of bookings: {queryset.count()}")
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"{self.request.user.username}  \u2192  Booking Panel"
        return context

class UserBookingUpdateView(LoginRequiredMixin, UpdateView):
    model = Booking
    fields = ['num_seats']
    template_name = 'Activities/new_activity.html'

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('user_event_booking_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"update booking for '{self.get_object().event.name}' event"
        return context
    
    def form_invalid(self, form):
        print(form.errors.as_data())
        context = self.get_context_data(form=form)
        context['error_message'] = "There was an error updating your booking." 
        return self.render_to_response(context)
    
class UserBookingDeleteView(LoginRequiredMixin, DeleteView):
    model = Booking
    template_name = 'Activities/event_bookings.html'
    success_url = reverse_lazy('user_event_booking_list')
# BOOKING USER VIEWS  ______________________________________________

# ADMIN -> BOOKING VIEWS  ______________________________________________
class EventBookingsView(LoginRequiredMixin, CultureGroupRequiredMixin, DetailView):
    model = Event
    template_name = 'Activities/event_bookings.html'
    context_object_name = 'evento'
    pk_url_kwarg = 'evento_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Booking.objects.filter(event=self.object)
        context['title'] = f"{self.object.name} \u2192 All Bookings"
        return context
# ADMIN -> BOOKING VIEWS  ______________________________________________

