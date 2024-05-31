from datetime import timedelta
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Event, Course, Booking, Subscription
from braces.views import GroupRequiredMixin
from django.contrib import messages
from .forms import BookingForm, EventForm, SearchForm, CourseForm, SubscriptionForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from django.utils import timezone


def aboutAs_view(request):
    context = {'title': 'About Us - SpritzCollege'}
    return render(request, 'about.html', context)


class CultureGroupRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='culture').exists()


def string_for_title(search_string, search_where, status, start_date, end_date):
    out = "Searching for "

    if search_string:
        out += f"{search_where} containing '{search_string}'"
    if status:
        if search_string:
            out += f", status [{status}]"
        else:
            out = f"events with status [{status}]"
    if start_date and end_date:
        if search_string or status:
            out += f", from {start_date} to {end_date}"
        else:
            out = f"events from {start_date} to {end_date}"

    if not search_string and not status and (start_date or end_date):
        out = "events"
        if start_date and end_date:
            out += f" from {start_date} to {end_date}"
        elif start_date:
            out += f" from {start_date}"
        elif end_date:
            out += f" to {end_date}"

    return out


class EventsList(ListView):
    model = Event
    template_name = "Activities/Events/events.html"

    def get_queryset(self):
        full_queryset = super().get_queryset()
        filtered_queryset = super().get_queryset()

        search_string = self.request.GET.get("search_string", "")
        search_where = self.request.GET.get("search_where", "")
        status = self.request.GET.get("status", "")

        start_date = self.request.GET.get("start_date", "")
        end_date = self.request.GET.get("end_date", "")

        print("Parametri di ricerca: \n")
        print(f"stringa: {search_string}")
        print(f"dove: {search_where}")
        print(f"stato: {status}")

        search_performed = False

        if search_string and search_where:
            search_performed = True
            if search_where == "Name":
                filtered_queryset = full_queryset.filter(
                    name__icontains=search_string, status=status)
            elif search_where == "Description":
                filtered_queryset = full_queryset.filter(
                    description__icontains=search_string, status=status)

        if status:
            search_performed = True
            filtered_queryset = filtered_queryset.filter(status=status)

        if start_date and end_date:
            search_performed = True
            try:
                start_date = timezone.datetime.strptime(
                    start_date, "%Y-%m-%d").date()
                end_date = timezone.datetime.strptime(
                    end_date, "%Y-%m-%d").date()
                filtered_queryset = filtered_queryset.filter(
                    date__date__range=(start_date, end_date))
            except ValueError:
                messages.add_message(
                    self.request, messages.ERROR, 'Invalid date format. Please use YYYY-MM-DD.')

        if not filtered_queryset.exists() and search_performed:
            messages.add_message(self.request, messages.INFO,
                                 'No results found for your search criteria.')
            return full_queryset

        self.filtered_queryset = filtered_queryset
        self.search_performed = search_performed
        return filtered_queryset

    def get_context_data(self, **kwargs):
        context = super(EventsList, self).get_context_data(**kwargs)
        context['form'] = SearchForm(self.request.GET or None)
        context['title'] = "Events"

        if hasattr(self, 'filtered_queryset') and self.filtered_queryset.exists() and self.search_performed:
            # out = string_for_title (self.request.GET.get("search_string", ""), self.request.GET.get("status", ""))
            context['criteria'] = string_for_title(
                self.request.GET.get("search_string", ""),
                self.request.GET.get("search_where", ""),
                self.request.GET.get("status", ""),
                self.request.GET.get("start_date", ""),
                self.request.GET.get("end_date", "")
            )
            # context['criteria'] = string_for_title (self.request.GET.get("search_string", ""), self.request.GET.get("status", ""), self.request.GET.get("start_date", ""), self.request.GET.get("end_date", ""))
            context['title'] = "Results - Events"

        return context


class CoursesList(ListView):
    model = Course
    template_name = "Activities/Courses/courses.html"

    def get_context_data(self, **kwargs):
        context = super(CoursesList, self).get_context_data(**kwargs)
        context['title'] = "Courses"
        return context

# * EVENTS


class AddEvents(GroupRequiredMixin, CreateView):
    group_required = ["culture"]
    form_class = EventForm
    template_name = "Activities/master_activity.html"
    success_url = reverse_lazy("list_events")

    def form_valid(self, form):
        response = super().form_valid(form)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "New Event - SpritzCollege"
        return context


class EventDetail(DetailView):
    model = Event
    template_name = 'Activities/Events/event_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['available_seats'] = self.object.available_seats
        return context


class EventUpdateView(CultureGroupRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'Activities/master_activity.html'
    success_url = reverse_lazy('list_events')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f' {self.get_object().name} \u2192 Update Event'
        return context


class EventDeleteView(CultureGroupRequiredMixin, DeleteView):
    model = Event
    success_url = reverse_lazy('list_events')
    template_name = 'Activities/event_detail.html'

# * COURSES


class AddCourse (GroupRequiredMixin, CreateView):
    group_required = ["culture"]
    form_class = CourseForm
    template_name = "Activities/master_activity.html"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "New Course - SpritzCollege"
        return context


class CourseDetail(DetailView):
    model = Course
    template_name = 'Activities/Courses/course_detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CourseUpdateView(CultureGroupRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'Activities/master_activity.html'
    success_url = reverse_lazy('list_courses')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Course'
        return context


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


# new booking ____________________________________________
'''@login_required
def book_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = BookingForm(request.POST, initial={'event': event})
        if form.is_valid():
                booking = form.save(commit=False)
                booking.user = request.user
                booking.event = event
                try:
                    booking.save()
                    messages.success(request, 'Your booking was successful!')
                    return redirect('event_detail', pk=event.id)
                except ValidationError as e:
                    form.add_error(None, e)
        else: 
            error_message = form.errors.as_text()
            return render(request, 'Activities/master_activity.html', {
            'form': form,
            'event': event,
            'popup': True,
            'message': f'[{error_message}]<br><br>There was an error with your booking. Please check your data and try again.<br><br>You will be returned to the previous page.',
            'redirect_url': reverse('event_detail', kwargs={'pk': event.id})
        })
    else:
        form = BookingForm(initial={'event': event})
    return render(request, 'Activities/master_activity.html', {'title': f'{event.name} \u2192 Book Event', 'form': form, 'event': event})
'''


@login_required
def book_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = BookingForm(request.POST, request=request)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.event = event
            try:
                booking.save()
                messages.success(request, 'Your booking was successful!')
                return redirect('event_detail', pk=event.id)
            except ValidationError as e:
                form.add_error(None, e)
        else:
            error_message = form.errors.as_text()
            return render(request, 'Activities/master_activity.html', {
                'form': form,
                'event': event,
                'popup': True,
                'message': f'[{error_message}]<br><br>There was an error with your booking. Please check your data and try again.<br><br>You will be returned to the previous page.',
                'redirect_url': reverse('event_detail', kwargs={'pk': event.id})
            })
    else:
        form = BookingForm(initial={'event': event}, request=request)
    return render(request, 'Activities/master_activity.html', {'title': f'{event.name} \u2192 Book Event', 'form': form, 'event': event})

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
    template_name = 'Activities/Events/event_bookings.html'

    def get_queryset(self):
        queryset = Booking.objects.filter(
            user=self.request.user).order_by('event__date')
        # print(f"Number of bookings: {queryset.count()}")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"{
            self.request.user.username}  \u2192  Booking Panel"
        context['view_type'] = "user"
        return context

# BOOKING USER VIEWS  ______________________________________________

# ADMIN -> BOOKING VIEWS  ______________________________________________


class EventBookingsView(LoginRequiredMixin, CultureGroupRequiredMixin, DetailView):
    model = Event
    template_name = 'Activities/Events/event_bookings.html'
    context_object_name = 'evento'
    pk_url_kwarg = 'evento_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Booking.objects.filter(event=self.object)
        context['view_type'] = "admin"
        context['title'] = f"{self.object.name} \u2192 All Bookings"
        return context
# ADMIN -> BOOKING VIEWS  ______________________________________________


class BookingUpdateMixin:
    model = Booking
    form_class = BookingForm
    template_name = 'Activities/master_activity.html'

    def form_valid(self, form):
        return super().form_valid(form)

    def get_queryset(self):
        event_id = self.kwargs.get('event_id')
        if self.request.user.is_superuser or self.request.user.groups.filter(name='culture').exists():
            if event_id:
                return Booking.objects.filter(event__id=event_id)
            return Booking.objects.all()
        return Booking.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_type'] = 'no_type'
        return context


@method_decorator(login_required, name='dispatch')
class UserBookingUpdateView(BookingUpdateMixin, UpdateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_type'] = 'user'
        return context

    def form_invalid(self, form):
        error_message = form.errors.as_text()
        context = self.get_context_data(form=form)
        context.update({
            'popup': True,
            'redirect_url': reverse('user_event_booking_list'),
            'message': f'[{error_message}]<br><br>There was an error with your booking. Please check your data and try again.<br><br>You will be returned to the previous page.'
        })
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse_lazy('user_event_booking_list')


@method_decorator(login_required, name='dispatch')
class AdminBookingUpdateView(BookingUpdateMixin, UpdateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_type'] = 'admin'
        return context

    def form_invalid(self, form):
        event_id = self.object.event.id
        error_message = form.errors.as_text()
        context = self.get_context_data(form=form)
        context.update({
            'popup': True,
            'redirect_url': reverse_lazy('bookings_view', kwargs={'evento_id': event_id}),
            'message': f'[{error_message}]<br><br>There was an error with your booking. Please check your data and try again.<br><br>You will be returned to the previous page.'
        })
        return self.render_to_response(context)

    def get_success_url(self):
        event_id = self.object.event.id
        return reverse_lazy('bookings_view', kwargs={'evento_id': event_id})


class AdminBookingDeleteView(CultureGroupRequiredMixin, DeleteView):
    model = Booking
    template_name = 'Activities/Events/event_bookings.html'

    def get_success_url(self):
        evento_id = self.object.event.id
        return reverse_lazy('bookings_view', kwargs={'evento_id': evento_id})

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class UserBookingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Booking
    template_name = 'Activities/Events/event_bookings.html'
    success_url = reverse_lazy('user_event_booking_list')

    # print ("siamo qui")

    def test_func(self):
        self.object = self.get_object()
        return self.object.user == self.request.user

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Prenotazione cancellata con successo!")
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return super().get_success_url()


def course_pdf(request, course_id):
    course = Course.objects.get(id=course_id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{
        course.name}.pdf"'

    p = canvas.Canvas(response)
    user = request.user if request.user.is_authenticated else None

    image_height = 3 * inch
    image_y_position = 800 - image_height

    if course.image and hasattr(course.image, 'path'):
        try:
            p.drawImage(course.image.path, 100, image_y_position, width=4*inch,
                        height=image_height, preserveAspectRatio=True, mask='auto')
        except Exception as e:
            print(f"Error loading image: {e}")

    text_start_position = image_y_position - 30

    p.setFont("Helvetica", 16)
    p.drawString(100, text_start_position, course.name)

    if user:
        p.setFont("Helvetica", 12)
        p.drawString(100, text_start_position - 20, f"Requested by: {
                     user.username} on {timezone.localtime().strftime('%Y-%m-%d %H:%M')}")

    p.setFont("Helvetica", 12)
    p.drawString(100, text_start_position - 40,
                 f"Duration: {course.start_date} to {course.end_date}")
    p.drawString(100, text_start_position - 60,
                 f"Category: {course.get_category_display()}")

    p.showPage()
    p.save()
    return response

# USER -> SUBSCRIBE VIEWS  ______________________________________________


class SubscriptionCreateView(LoginRequiredMixin, CreateView):
    model = Subscription
    form_class = SubscriptionForm
    template_name = 'Activities/master_activity.html'
    success_url = reverse_lazy('subscription_list')

    def get_initial(self):
        initial = super().get_initial()
        course_id = self.kwargs.get('course_id')
        if course_id:
            initial['course'] = get_object_or_404(Course, pk=course_id)
        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Subscribe Course - SpritzCollege'
        return context


class SubscriptionListView(LoginRequiredMixin, ListView):
    model = Subscription
    template_name = 'Activities/Courses/course_subscriptions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"{
            self.request.user.username}  \u2192  Courses Panel"
        return context


class SubscriptionUpdateView(UpdateView):
    model = Subscription
    fields = ['user', 'course']
    template_name = 'subscriptions/subscription_form.html'
    success_url = reverse_lazy('subscription_list')

    def form_valid(self, form):
        return super().form_valid(form)


class SubscriptionDeleteView(DeleteView):
    model = Subscription
    template_name = 'subscriptions/subscription_confirm_delete.html'
    success_url = reverse_lazy('subscription_list')
# USER -> SUBSCRIBE VIEWS  ______________________________________________


class CourseSubscriptionListView(LoginRequiredMixin, ListView):
    model = Subscription
    template_name = 'Activities/Courses/course_subscriptions2.html'
    context_object_name = 'subscriptions'

    def get_queryset(self):
        course_id = self.kwargs.get('course_id')
        return Subscription.objects.filter(course__id=course_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        context['course'] = course
        return context
