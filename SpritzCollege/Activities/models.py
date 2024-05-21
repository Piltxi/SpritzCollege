from decimal import Decimal
from django.db import models
from django.forms import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User

from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User
from decimal import Decimal

class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    date = models.DateTimeField()
    duration = models.DurationField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_capacity = models.IntegerField(default=100)
    place = models.CharField(max_length=100, default="conference room")
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('cancelled', 'Cancelled'), ('completed', 'Completed')], default='active')

    def is_free(self):
        return self.price is None or self.price == Decimal('0.00')

    def clean(self):
        if self.date < timezone.now():
            raise ValidationError('La data non può essere nel passato.')

    def __str__(self):
        return f"{self.name} ({self.date.strftime('%Y-%m-%d %H:%M')})"

    class Meta:
        ordering = ['date']

class Booking(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    num_seats = models.PositiveIntegerField()

    def clean(self):
        if self.event.status != 'active':
            raise ValidationError('Non è possibile prenotare un evento non attivo.')
        if self.event.date < timezone.now():
            raise ValidationError('Non è possibile prenotare un evento passato.')
        
        total_booked_seats = self.event.bookings.aggregate(models.Sum('num_seats'))['num_seats__sum'] or 0
        if self.num_seats > self.event.max_capacity - total_booked_seats:
            raise ValidationError('Non ci sono abbastanza posti disponibili per questa prenotazione.')

    def __str__(self):
        return f"Prenotazione di {self.user.username} per {self.event.name}"

    class Meta:
        unique_together = ('event', 'user')
        ordering = ['event', 'user']


class Course (models.Model):

    CATEGORY_CHOICES = [
        ('ANY', 'uncategorized'),
        ('TCH', 'tech course'),
        ('LTR', 'literature course'),
        ('LAN', 'language course'),
        ('HND', 'craftsman course'),
        ('ART', 'art course'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    start_date = models.DateField()
    end_date = models.DateField()
    recurrence_day = models.CharField(max_length=20)
    
    image = models.ImageField(upload_to='Courses', default='Courses/default.jpg')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='ANY')

    def __str__(self):
        return self.name