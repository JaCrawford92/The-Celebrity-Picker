from django import forms
from .models import UserProfile

class DateForm(forms.Form):
    selected_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Select a date"
    )

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['photo']
