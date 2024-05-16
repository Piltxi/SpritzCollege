from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.contrib.auth.models import User, Group

class VisitorRegistrationForm(UserCreationForm):
    bio = forms.CharField(label='Bio', max_length=500, required=False)
    location = forms.CharField(label='Location', max_length=30, required=False)
    birth_date = forms.DateField(label='Birth Date', required=False)
    profile_pic = forms.ImageField(label='Profile Picture', required=False)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'bio', 'location', 'birth_date', 'profile_pic']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Crea o aggiorna il profilo associato all'utente
            profile, created = Profile.objects.get_or_create(user=user)
            profile.bio = self.cleaned_data.get('bio', '')
            profile.location = self.cleaned_data.get('location', '')
            profile.birth_date = self.cleaned_data.get('birth_date', None)
            profile.profile_pic = self.cleaned_data.get('profile_pic', None)
            profile.save()
        return user

class UserGroupForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all())
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), widget=forms.CheckboxSelectMultiple)