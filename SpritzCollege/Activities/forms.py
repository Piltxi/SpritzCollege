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
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['event', 'num_seats']