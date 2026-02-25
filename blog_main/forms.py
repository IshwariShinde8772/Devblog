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
        email = self.cleaned_data.get('email')
        
        # Email regex pattern for stricter validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(email_pattern, email):
            raise forms.ValidationError('Please enter a valid email address (e.g., user@example.com)')
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        
        # Reject emails with more than one dot separation (like .com.in.edu)
        parts = email.split('@')
        if len(parts) != 2:
            raise forms.ValidationError('Invalid email format.')
        
        domain = parts[1]
        # Domain should have at most 2 parts separated by dot (e.g., example.com) 
        # This prevents things like gmail.com.in.edu
        domain_parts = domain.split('.')
        if len(domain_parts) > 3 or len(domain_parts) < 2:
            raise forms.ValidationError('Please use a valid email domain (e.g., gmail.com, company.co.uk).')
        
        return email