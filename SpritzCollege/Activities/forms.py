from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import *

class SearchForm (forms.Form):
    SEARCH_CHOICES = (
        ('Name', 'Name'),
        ('Description', 'Description'),
    )

    search_string = forms.CharField(max_length=100, required=False)
    search_where = forms.ChoiceField(choices=SEARCH_CHOICES, required=False)

class EventForm(forms.ModelForm):
       class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'price', 'max_capacity', 'place']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),  # Utilizza un widget per data e ora
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