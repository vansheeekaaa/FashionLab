from django import forms
from .models import DesignSubmission

class DesignForm(forms.ModelForm):
    class Meta:
        model = DesignSubmission
        fields = ['name', 'email', 'password', 'design_link']
        widgets = {
            'password': forms.PasswordInput(),
        }
