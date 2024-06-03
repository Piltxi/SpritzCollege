from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.views import View

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Sum

from datetime import timedelta
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
import openpyxl
from reportlab.pdfgen import canvas
from braces.views import GroupRequiredMixin
from io import BytesIO

from .models import Event, Course, Booking, Subscription
from .forms import BookingForm, EventForm, SearchForm, CourseForm, SubscriptionForm

class CultureGroupRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.groups.filter(name='culture').exists()


def str_criteriasearch(search_string, search_where, status, start_date, end_date):
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


# * ______________  ACTIVITIES::PUBLIC  _______________________________
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
            # out = str_criteriasearch (self.request.GET.get("search_string", ""), self.request.GET.get("status", ""))
            context['criteria'] = str_criteriasearch(
                self.request.GET.get("search_string", ""),
                self.request.GET.get("search_where", ""),
                self.request.GET.get("status", ""),
                self.request.GET.get("start_date", ""),
                self.request.GET.get("end_date", "")
            )
            # context['criteria'] = str_criteriasearch (self.request.GET.get("search_string", ""), self.request.GET.get("status", ""), self.request.GET.get("start_date", ""), self.request.GET.get("end_date", ""))
            context['title'] = "Results - Events"

        return context


class CoursesList(ListView):
    model = Course
    template_name = "Activities/Courses/courses.html"

    def get_context_data(self, **kwargs):
        context = super(CoursesList, self).get_context_data(**kwargs)
        context['title'] = "Courses"
        return context

def calendar_spritzcollege_view (request): 
    events = Event.objects.all()
    courses = Course.objects.all()
    return calendar_view(request, events, courses, None)

def generate_recurrence_dates(course):
    recurrence_dates = []
    current_date = course.start_date
    while current_date <= course.end_date:
        if current_date.strftime('%A').lower() == course.recurrence_day.lower():
            recurrence_dates.append(current_date)
        current_date += timedelta(days=1)
    return recurrence_dates

def calendar_view(request, events, courses, title):
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
        'calendar_data': calendar_data,
        'title': title if title else 'Calendar'
    }
    
    context['calendar_data'] = calendar_data
   
    return render(request, 'Activities/calendar.html', context)
# * ______________  ACTIVITIES::PUBLIC  _______________________________


# * ______________  EVENTS:: "Culture"  _______________________________
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
    template_name = 'Activities/Events/event_detail.html'
# * ______________  EVENTS:: "Culture"  _______________________________


# * ______________  COURSE:: "Culture"  _______________________________
class AddCourse (GroupRequiredMixin, CreateView):
    group_required = ["culture"]
    form_class = CourseForm
    template_name = "Activities/master_activity.html"
    success_url = reverse_lazy("list_courses")

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


class CourseUpdateView(GroupRequiredMixin, UpdateView):
    group_required = ["culture"]
    model = Course
    form_class = CourseForm
    template_name = 'Activities/master_activity.html'
    success_url = reverse_lazy('list_courses')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Course'
        return context


class CourseDeleteView(GroupRequiredMixin, DeleteView):
    group_required = ["culture"]
    model = Course
    success_url = reverse_lazy('list_courses')
    template_name = 'Activities/course_detail.html'
# * ______________  COURSE:: "Culture"  _______________________________


# * ______________  BOOKING:: "All"  _______________________________
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
                # return redirect('event_detail', pk=event.id)
                return redirect('user_event_booking_list')
            except ValidationError as e:
                form.add_error(None, e)
        else:
            error_message = form.errors.as_text()
            return render(request, 'Activities/master_activity.html', {
                'form': form,
                'event': event,
                'popup': True,
                'message': f'[{error_message}]<br><br>There was an error with your booking. Please check your data and try again.<br><br>You will be returned to the previous page.',
                # 'redirect_url': reverse('user_event_booking_list')
                'redirect_url': reverse('event_detail', kwargs={'pk': event.id})
            })
    else:
        form = BookingForm(initial={'event': event}, request=request)
    return render(request, 'Activities/master_activity.html', {'title': f'{event.name} \u2192 Book Event', 'form': form, 'event': event})

# * ______________  BOOKING:: "All"  _______________________________


# * ______________ BOOKING USER VIEWS ______________________________________________

@login_required
def generate_booking_pdf(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="booking_{booking_id}.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    p.setFillColor(colors.whitesmoke)
    p.rect(0, 0, width, height, fill=1)
    p.setStrokeColor(colors.grey)
    p.setLineWidth(3)
    p.rect(30, 30, width - 60, height - 60)

    p.setFont("Helvetica-Bold", 24)
    p.setFillColor(colors.darkblue)
    p.drawCentredString(width / 2.0, height - 100, "Booking Confirmation")

    p.setFont("Helvetica-Bold", 14)
    p.setFillColor(colors.black)
    p.drawString(100, height - 150, "User Information")
    p.setFont("Helvetica", 12)
    p.drawString(100, height - 170, f"Username: {booking.user.username}")
    p.drawString(100, height - 190, f"Email: {booking.user.email}")

    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, height - 230, "Event Information")
    p.setFont("Helvetica", 12)
    p.drawString(100, height - 250, f"Event: {booking.event.name}")
    p.drawString(100, height - 270, f"Description: {booking.event.description}")
    p.drawString(100, height - 290, f"Date: {booking.event.date.strftime('%Y-%m-%d %H:%M')}")
    p.drawString(100, height - 310, f"Place: {booking.event.place}")
    p.drawString(100, height - 330, f"Status: {booking.event.status}")

    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, height - 370, "Booking Information")
    p.setFont("Helvetica", 12)
    p.drawString(100, height - 390, f"Seats Booked: {booking.num_seats}")
    p.drawString(100, height - 410, f"Booking Date: {booking.booking_time.strftime('%Y-%m-%d %H:%M')}")

    p.setFont("Helvetica-Oblique", 12)
    p.setFillColor(colors.darkgreen)
    p.drawString(100, height - 450, "Thank you for booking with us!")

    p.setFont("Helvetica", 10)
    p.setFillColor(colors.grey)
    p.drawString(100, 50, "If you have any questions, please contact our support team.")

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response

@login_required
def calendar_user_view (request): 
    events = Event.objects.filter(bookings__user=request.user)
    courses = Course.objects.filter(subscribers__user=request.user)
    
    title = f"{request.user}'s calendar"
    
    return calendar_view(request, events, courses, title)

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


class UserBookingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Booking
    template_name = 'Activities/Events/event_bookings.html'
    success_url = reverse_lazy('user_event_booking_list')

    def test_func(self):
        self.object = self.get_object()
        return self.object.user == self.request.user

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Prenotazione cancellata con successo!")
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return super().get_success_url()
# * ______________ BOOKING USER VIEWS  ______________________________________________


# * ______________ ADMIN VIEWS  ______________________________________________
class AdminEventBookingsView(LoginRequiredMixin, CultureGroupRequiredMixin, DetailView):
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


class AdminBookingDeleteView(CultureGroupRequiredMixin, DeleteView):
    model = Booking
    template_name = 'Activities/Events/event_bookings.html'

    def get_success_url(self):
        evento_id = self.object.event.id
        return reverse_lazy('bookings_view', kwargs={'evento_id': evento_id})

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
# * ______________ ADMIN VIEWS  ______________________________________________


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


def course_brochure_pdf(request, course_id):
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

# * SUBSCRIBE::USER  ______________________________________________


class UserSubscriptionListView(LoginRequiredMixin, ListView):
    model = Subscription
    context_object_name = 'subscriptions'
    template_name = 'Activities/Courses/course_subscriptions.html'

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_type'] = "user"
        context['item'] = f"{
            self.request.user.username}"
        context['title'] = f"{
            self.request.user.username}  \u2192  Courses Panel"
        return context


@login_required
def subscribe_to_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        form = SubscriptionForm(request.POST, request=request)
        if form.is_valid():
            sub = form.save(commit=False)
            sub.user = request.user
            sub.course = course
            try:
                sub.save()
                messages.success(
                    request, 'Your subscription was successful, commit to attending classes!!')
                return redirect('subscription_list')
            except ValidationError as e:
                form.add_error(None, e)
        else:
            error_message = form.errors.as_text()
            return render(request, 'Activities/master_activity.html', {
                'form': form,
                'event': course,
                'popup': True,
                'message': f'[{error_message}]<br><br>There was an error with your sub. Please check your data and try again.<br><br>You will be returned to the previous page.',
                'redirect_url': reverse('course_detail', kwargs={'pk': course.id})
            })
    else:
        form = SubscriptionForm(initial={'course': course}, request=request)
    return render(request, 'Activities/master_activity.html', {'title': f'{course.name} \u2192 Enrolling', 'form': form, 'event': course})


class UserSubscriptionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Subscription
    template_name = 'Activities/Courses/course_subscriptions.html'
    success_url = reverse_lazy('subscription_list')

    def test_func(self):
        self.object = self.get_object()
        return self.object.user == self.request.user

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Iscrizione cancellata con successo!")
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return super().get_success_url()
# * SUBSCRIBE::USER  ______________________________________________


# * SUBSCRIBE:: "Culture"  ______________________________________________

class CourseSubscriptionListView(CultureGroupRequiredMixin, ListView):
    model = Subscription
    template_name = 'Activities/Courses/course_subscriptions.html'
    context_object_name = 'subscriptions'

    def get_queryset(self):
        course_id = self.kwargs.get('course_id')
        return Subscription.objects.filter(course__id=course_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        context['item'] = f"{course.name}"
        context['title'] = f"{course.name} \u2192 All Subscriptions"
        context['course'] = course
        context['view_type'] = "admin"
        return context


class ExportCourseSubscriptionsExcelView(CultureGroupRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        course_id = self.kwargs.get('course_id')
        course = get_object_or_404(Course, id=course_id)
        subscriptions = Subscription.objects.filter(course=course)

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = f"Subscriptions for {course.name}"

        headers = ['Username', 'Subscription Date']
        ws.append(headers)

        for subscription in subscriptions:
            ws.append([
                subscription.user.username,
                subscription.subscription_date.strftime("%d/%m/%Y %H:%M")
            ])

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename=Subscriptions_{
            course.name}.xlsx'
        wb.save(response)
        return response


class AdminUserSubscriptionDeleteView(CultureGroupRequiredMixin, DeleteView):
    model = Subscription
    template_name = 'Activities/Courses/course_subscriptions.html'

    def get_success_url(self):
        course_id = self.object.course.id
        return reverse_lazy('course_subscriptions', kwargs={'course_id': course_id})

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


# * SUBSCRIBE:: "Culture"  ______________________________________________

class ExportActiveEventsToExcelView(CultureGroupRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        events = Event.get_active_events().annotate(num_bookings=Sum('bookings__num_seats'))

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Active Events"

        headers = [
            'Event Name', 'Description', 'Date', 'Duration', 'Price', 'Max Capacity',
            'Place', 'Status', 'Number of Bookings', 'Available Seats'
        ]
        ws.append(headers)

        for event in events:
            ws.append([
                event.name,
                event.description,
                event.date.strftime('%Y-%m-%d %H:%M'),
                str(event.duration),
                str(event.price),
                event.max_capacity,
                event.place,
                event.status,
                event.num_bookings or 0,
                event.available_seats
            ])

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=active_events.xlsx'
        wb.save(response)

        return response