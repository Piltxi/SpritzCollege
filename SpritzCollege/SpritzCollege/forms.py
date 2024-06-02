from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.contrib import messages

class CustomAuthenticationForm(AuthenticationForm):
    def clean(self):
        super().clean()

        if self.errors:
            raise forms.ValidationError(
                messages.error(self.request, _("Login non riuscito. Si prega di verificare le credenziali e riprovare.")),
            )
