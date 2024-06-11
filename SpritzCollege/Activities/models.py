from django.db import models
from django.forms import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Q, Sum, F, ExpressionWrapper

from datetime import timedelta
from decimal import Decimal
import os

def course_image_path(instance, filename):
    return f"Courses/{instance.id}/{filename}"

def default_event_time():
    return (timezone.localtime(timezone.now()) + timedelta(hours=1)).replace(second=0, microsecond=0)

class Event(models.Model):
    ACTIVE = 'active'
    CANCELLED = 'cancelled'
    COMPLETED = 'completed'

    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (CANCELLED, 'Cancelled'),
        (COMPLETED, 'Completed'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    date = models.DateTimeField(default=default_event_time)
    duration = models.DurationField(default=timedelta(hours=1))
    price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, default=Decimal('0.00'))
    max_capacity = models.PositiveIntegerField(default=100)
    place = models.CharField(max_length=100, default="conference room")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=ACTIVE)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    @property
    def available_seats(self):
        total_booked_seats = self.bookings.aggregate(
            Sum('num_seats'))['num_seats__sum'] or 0
        return self.max_capacity - total_booked_seats

    @property
    def is_free(self):
        return self.price is None or self.price == Decimal('0.00')

    def clean(self):
        if self._state.adding and self.date < timezone.now():
            raise ValidationError('It is not possible to book a past event!')

        if self.duration and self.duration.total_seconds() < 60:
            raise ValidationError(
                'Event duration must be at least one minute!')

        end_time = self.date + self.duration

        events_with_end_time = Event.objects.annotate(
            end_time=ExpressionWrapper(
                F('date') + F('duration') + timedelta(minutes=10), output_field=models.DateTimeField())
        )

        overlapping_events = events_with_end_time.filter(
            place=self.place,
            status=Event.ACTIVE
        ).filter(
            Q(date__lt=end_time) & Q(end_time__gt=self.date)
        ).exclude(id=self.id)

        if overlapping_events.exists():
            raise ValidationError(
                'Another event is scheduled in the same place at the same time!')

        if self.price < 0:
            raise ValidationError('The price must be zero or higher!')

    @classmethod
    def get_active_events(cls):
        return cls.objects.filter(status=cls.ACTIVE)

    @classmethod
    def get_upcoming_events(cls):
        return cls.objects.filter(date__gte=timezone.now())

    def __str__(self):
        local_date = timezone.localtime(self.date)
        return f"{self.name} ({local_date.strftime('%Y-%m-%d %H:%M')})"

    class Meta:
        ordering = ['date']

class Booking(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    num_seats = models.PositiveIntegerField(default=1)
    booking_time = models.DateTimeField(auto_now_add=True)

    def clean(self):
        event_end_time = self.event.date + self.event.duration

        if self.num_seats <= 0:
            raise ValidationError('Impossible to reserve zero seats!')

        if self.event.status != 'active':
            raise ValidationError(
                'It is not possible to book an inactive event!')

        if self.event.date < timezone.now():
            raise ValidationError('It is not possible to book a past event!')

        total_booked_seats = self.event.bookings.aggregate(
            models.Sum('num_seats'))['num_seats__sum'] or 0
        if self.num_seats > self.event.max_capacity - total_booked_seats:
            raise ValidationError('There are not enough seats available!')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Prenotazione di {self.user.username} per {self.event.name}"

    class Meta:
        unique_together = ('event', 'user', 'booking_time')
        ordering = ['event', 'user']


class Course(models.Model):
    CATEGORY_CHOICES = [
        ('ANY', 'uncategorized'),
        ('TCH', 'tech course'),
        ('LTR', 'literature course'),
        ('LAN', 'language course'),
        ('HND', 'craftsman course'),
        ('ART', 'art course'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    recurrence_day = models.CharField(max_length=20)
    time = models.TimeField()
    image = models.ImageField(default='default_course.jpeg')
    category = models.CharField(
        max_length=50, choices=CATEGORY_CHOICES, default='ANY')
        
    def save(self, *args, **kwargs):
        self.clean()
        
        if not self.id:
            temp_image = self.image
            self.image = None
            super().save(*args, **kwargs)
            self.image = temp_image

        if self.image and 'default_course.jpeg' not in self.image.path:
            self.image.name = course_image_path(self, self.image.name)

        super().save(*args, **kwargs)
        
    def clean (self): 
        if self.end_date < self.start_date:
            raise ValidationError('The end date must be greater than the start date!')

    def __str__(self):
        return self.name

class Subscription(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='course_subscriptions')
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='subscribers')
    subscription_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f'{self.user.username} subscribed to {self.course.name}'

    def clean(self):
        if self.course.start_date < timezone.now().date():
            raise ValidationError(
                "It is not possible to enroll in a course that has already started!")
