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

    search_string = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'about events'}), label='ask for something',)
    search_where = forms.ChoiceField(choices=SEARCH_CHOICES, required=False, label='field')
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False, initial='active', label='status')


class EventForm(forms.ModelForm):
       class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'price', 'max_capacity', 'place']
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
    
    recurrence_day = forms.ChoiceField(choices=DAYS_OF_WEEK, widget=forms.Select())
    
    class Meta:
        model = Course
        fields = ['name', 'description', 'start_date', 'end_date', 'recurrence_day', 'time', 'image', 'category']
        
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
        super(BookingForm, self).__init__(*args, **kwargs)
        self.fields['num_seats'].initial = 1
        
class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['course', 'email']
        widgets = {
            'email': forms.EmailInput(attrs={'style': 'width: 300px; height: 40px;'}),
        }