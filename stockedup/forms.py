from django import forms
from registration.forms import RegistrationForm

class MyRegForm(RegistrationForm):
    username = forms.CharField(max_length=254, required=False, widget=forms.HiddenInput())

    def clean_email(self):
        email = self.cleaned_data['email']
        self.cleaned_data['username'] = email
        return email

    error_messages = {}
