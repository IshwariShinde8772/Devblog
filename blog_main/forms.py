from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
import re


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text='Enter a valid email address'
    )
    
    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')
    
    def clean_email(self):
        email = (self.cleaned_data.get('email') or '').strip().lower()

        # Basic email regex pattern
        email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'

        if not re.match(email_pattern, email):
            raise forms.ValidationError('Please enter a valid email address (e.g., user@example.com)')

        # Split local and domain parts explicitly
        parts = email.split('@')
        if len(parts) != 2:
            raise forms.ValidationError('Invalid email format.')

        domain = parts[1]
        domain_parts = [p for p in domain.split('.') if p]

        # Require at least 'example.com' (2 parts) and at most 3 parts (e.g., company.co.uk)
        if len(domain_parts) < 2 or len(domain_parts) > 3:
            raise forms.ValidationError('Please use a valid email domain (e.g., gmail.com, company.co.uk).')

        # Case-insensitive duplicate check
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('This email is already registered.')

        return email