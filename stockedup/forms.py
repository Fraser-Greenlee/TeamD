from django import forms
from registration.forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm

class MyRegForm(RegistrationForm):

    def clean_email(self):
        email = self.cleaned_data['email']
        self.cleaned_data['username'] = email
        return email

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        # remove username
        self.fields.pop('username')
