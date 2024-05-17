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