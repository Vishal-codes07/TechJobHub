from django import forms

from .models import Job


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'company_name', 'description', 'location', 'salary']
        labels = {'salary': 'Salary (₹)'}
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g. Python Developer'}),
            'company_name': forms.TextInput(attrs={'placeholder': 'e.g. Acme Technologies'}),
            'location': forms.TextInput(attrs={'placeholder': 'e.g. Gurugram, Haryana'}),
            'salary': forms.NumberInput(attrs={'placeholder': 'e.g. 600000', 'min': 0}),
            'description': forms.Textarea(attrs={'rows': 8, 'placeholder': 'Responsibilities, skills required, perks...'}),
        }
