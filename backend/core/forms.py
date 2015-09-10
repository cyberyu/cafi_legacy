from django import forms
from django.contrib.auth.models import User
from core.models import UserProfile
from django.conf import settings

required_validator = {
    'first_name': 'Your first name is required.',
    'last_name': 'Your last name is required.',
    'password' : 'Password is required.',
    'title': 'Your title is required.',
    'email': 'Please enter an authorized email address.',
    'email_dupe': 'This email address is already in use.',
    'office_phone': 'Your office phone number is required.',
}

def valid_domain(email):
    valid_domain = False
    for domain in settings.VALID_DOMAINS:
        if email.endswith(domain):
            valid_domain = True

    return valid_domain

def email_exists(email):
    if len(User.objects.filter(email=email)) > 0:
        return True
    else:
        return False

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')

    def clean_email(self):
        email = self.cleaned_data['email']
        if not valid_domain(email):
            raise forms.ValidationError(required_validator['email'])
        if email_exists(email):
            raise forms.ValidationError(required_validator['email_dupe'])
        return email

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('title', 'office_phone')
