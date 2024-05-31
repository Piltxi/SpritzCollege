from datetime import datetime
from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from .forms import BookingForm
from .models import Event, Booking
from django.contrib.auth.models import User
from Profiles.models import Profile

import pytz
from decimal import Decimal


class EventModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            'testuser', 'testuser@example.com', 'testpassword')
        cls.profile = Profile.objects.create(
            user=cls.user,
            bio="TEST BIO",
            location="Modena",
            birth_date="2001-11-10",
            interests="Tecnologia, Arte"
        )
        cls.event = Event.objects.create(
            name="Inauguration of the 2025 budget year of the Computerized Pharmacies Union",
            description="Event with the entire board of directors of the consortium to discuss the budget.",
            date=timezone.now() + timezone.timedelta(days=1),
            place="conference room",
            max_capacity=100,
            price=Decimal('10.00')
        )

    def test_max_available_seats(self):
        self.assertEqual(self.event.available_seats, 100)

    def test_max_available_seats_after_booking(self):
        Booking.objects.create(event=self.event, num_seats=50, user=self.user)
        self.assertEqual(self.event.available_seats, 50)

    def test_default_event_time(self):
        future_time = timezone.localtime(
            timezone.now() + timezone.timedelta(hours=1))
        future_time = future_time.replace(second=0, microsecond=0)
        event = Event.objects.create(name="Event with Default Time")
        self.assertAlmostEqual(event.date, future_time,
                               delta=timezone.timedelta(seconds=1))

    def test_event_overlap_validation(self):
        overlapping_event = Event(
            name="Second Event",
            description="This should fail",
            date=self.event.date,
            place=self.event.place
        )
        with self.assertRaises(ValidationError):
            overlapping_event.full_clean()

    def test_minimum_duration_validation(self):
        short_duration = timezone.timedelta(seconds=30)
        event = Event(
            name="Short Event",
            date=timezone.now() + timezone.timedelta(days=2),
            duration=short_duration
        )
        with self.assertRaises(ValidationError):
            event.full_clean()

    def test_past_event_creation(self):
        past_date = timezone.now() - timezone.timedelta(days=1)
        event = Event(
            name="Past Event",
            date=past_date
        )
        with self.assertRaises(ValidationError):
            event.full_clean()

    def test_negative_price(self):
        with self.assertRaises(ValidationError):
            event = Event(
                name="Negative Price Event",
                date=timezone.now() + timezone.timedelta(days=1),
                price=Decimal('-1.00')
            )
            event.full_clean()

    def test_event_is_free(self):
        free_event = Event.objects.create(
            name="Free Event",
            date=timezone.now() + timezone.timedelta(days=3),
            price=Decimal('0.00')
        )
        self.assertTrue(free_event.is_free)
        free_event.delete()

        paid_event = Event.objects.create(
            name="Paid Event",
            date=timezone.now() + timezone.timedelta(days=3),
            price=Decimal('1.00')
        )
        self.assertFalse(paid_event.is_free)

    def test_booking_overlap(self):
        overlapping_event = Event(
            name="Overlapping Event",
            description="This event overlaps with the first event",
            date=self.event.date,
            duration=timezone.timedelta(hours=2),
            place="conference room"
        )

        with self.assertRaises(ValidationError):
            overlapping_event.full_clean()

    def test_non_overlapping_booking(self):
        non_overlapping_event = Event.objects.create(
            name="Non-Overlapping Event",
            description="This event does not overlap with the first event",
            date=self.event.date + timezone.timedelta(days=1),
            duration=timezone.timedelta(hours=2),
            place="conference room"
        )

        booking = Booking(event=non_overlapping_event,
                          user=self.user, num_seats=1)
        try:
            booking.full_clean()
        except ValidationError:
            self.fail(
                "Booking for a non-overlapping event raised ValidationError unexpectedly!")

    def test_user_overlapping_booking(self):
        timezone = pytz.timezone('Europe/Rome')
        ev1 = Event.objects.create(
            name="Event Test 1",
            date=datetime(year=2024, month=6, day=12, hour=8,
                          minute=31, tzinfo=timezone),
            place="conference room",
            description="ev1 for booking test",
            price=Decimal('0.00')
        )

        bk1 = Booking(event=ev1, user=self.user, num_seats=2)
        bk1.save()

        ev2 = Event.objects.create(
            name="Event Test 2",
            date=datetime(year=2024, month=6, day=12, hour=8,
                          minute=31, tzinfo=timezone),
            place="cinema",
            description="ev2 for booking test",
            price=Decimal('0.00')
        )

        data = {
            'event': ev2.id,
            'num_seats': 1
        }

        form = BookingForm(data=data)
        form.request = type('Request', (object,), {'user': self.user})()

        is_valid = form.is_valid()

        with self.assertRaises(ValidationError) as context:
            form.clean()

        self.assertIn('You already have a booking for another event during this time.', str(
            context.exception))
