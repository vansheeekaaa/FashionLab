from django import forms
from .models import DesignSubmission
from django.contrib.auth.models import User

class DesignForm(forms.ModelForm):
    class Meta:
        model = DesignSubmission
        fields = ['name', 'email', 'design_link']

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    name = forms.CharField(max_length=100, required=True)  # Add this line

    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data