from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from .models import Profile
from django.contrib.auth.models import User, Group

class VisitorRegistrationForm(UserCreationForm):
    interests = forms.MultipleChoiceField(
        choices=Profile.CATEGORY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    bio = forms.CharField(label='Bio', widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}), max_length=500, required=False)
    location = forms.CharField(label='Locality', max_length=30, required=False)
    birth_date = forms.DateField(label='Date of Birth', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    profile_pic = forms.ImageField(label='Profile Pic', required=False)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']

    def clean_interests(self):
        return ','.join(self.cleaned_data['interests'])

    def __init__(self, *args, **kwargs):
        super(VisitorRegistrationForm, self).__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, 'profile'):
            profile = self.instance.profile
            initial_interests = profile.interests
            if initial_interests:
                self.fields['interests'].initial = initial_interests.split(',')

    def save(self, commit=True):
        user = super().save(commit=commit)
        profile, created = Profile.objects.get_or_create(user=user)
        profile.bio = self.cleaned_data.get('bio', '')
        profile.location = self.cleaned_data.get('location', '')
        profile.birth_date = self.cleaned_data.get('birth_date', None)
        profile.profile_pic = self.cleaned_data.get('profile_pic', None)
        profile.interests = self.cleaned_data.get('interests', '')
        if commit:
            profile.save()
        return user
    
class UserGroupForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all())
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), widget=forms.CheckboxSelectMultiple)
    
    def __init__(self, *args, **kwargs):
        user_instance = kwargs.pop('user_instance', None)
        super().__init__(*args, **kwargs)
        
        if user_instance:
            print (f"Campi ric: {user_instance.groups.all()}")
            self.fields['groups'].queryset = user_instance.groups.all()
    
class GroupMembershipForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all())
    group = forms.ModelChoiceField(queryset=Group.objects.all())
    action = forms.ChoiceField(choices=(('add', 'Add'), ('remove', 'Remove')))

    def __init__(self, *args, **kwargs):
        super(GroupMembershipForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget.attrs['onchange'] = 'this.form.submit()'

    def set_user_groups(self, user):
        self.fields['group'].queryset = Group.objects.exclude(user=user)
        self.fields['group'].initial = user.groups.all()
        
class ProfileForm(forms.ModelForm):
    interests = forms.MultipleChoiceField(
        choices=Profile.CATEGORY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Profile
        fields = ['bio', 'location', 'birth_date', 'profile_pic', 'interests']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            initial_interests = self.instance.interests
            if initial_interests:
                self.fields['interests'].initial = initial_interests.split(',')

    def clean_interests(self):
        return ','.join(self.cleaned_data['interests'])

class CustomPasswordChangeForm(PasswordChangeForm):
    pass