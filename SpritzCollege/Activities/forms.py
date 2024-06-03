from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import *


class SearchForm(forms.Form):
    SEARCH_CHOICES = (
        ('Name', 'Name'),
        ('Description', 'Description'),
    )
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    )

    search_string = forms.CharField(max_length=100, required=False, widget=forms.TextInput(
        attrs={'placeholder': 'about events'}), label='ask for something',)
    search_where = forms.ChoiceField(
        choices=SEARCH_CHOICES, required=False, label='field')
    status = forms.ChoiceField(
        choices=STATUS_CHOICES, required=False, initial='active', label='status')

    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=timezone.now().date(),
        label='Start Date'
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=(timezone.now() + timezone.timedelta(days=30)).date(),
        label='End Date'
    )


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date',
                  'price', 'max_capacity', 'place']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 60}),
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class CourseForm(forms.ModelForm):
    DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]

    recurrence_day = forms.ChoiceField(
        choices=DAYS_OF_WEEK, widget=forms.Select())

    class Meta:
        model = Course
        fields = ['name', 'description', 'start_date', 'end_date',
                  'recurrence_day', 'time', 'image', 'category']

        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['event', 'num_seats']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(BookingForm, self).__init__(*args, **kwargs)
        self.fields['num_seats'].initial = 1

    def clean(self):
        cleaned_data = super().clean()
        user = self.request.user if self.request else None
        event = cleaned_data.get('event')
        event_end_time = (event.date + event.duration) if event else None

        if user and event:
            if Booking.objects.filter(
                user=user,
                event__date__lt=(event.date + event.duration),
                event__date__gte=event.date
            ).exclude(event=event).exists():
                raise ValidationError(
                    'You already have a booking for another event during this time.')

        return cleaned_data


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['course']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(SubscriptionForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        user = self.request.user if self.request else None
        print(f"\n\nFORM: {user}\n\n\n")
        course = cleaned_data.get('course')

        if Subscription.objects.filter(user=user, course=course).exists():
            raise forms.ValidationError(
                "You are already subscribed to this course!")
        return cleaned_data
