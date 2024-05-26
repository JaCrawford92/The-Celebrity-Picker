from django import forms
from .models import UserProfile

class DateForm(forms.Form):
    selected_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
            }
        ),
        required=True,
    )

    def clean_selected_date(self):
        date = self.cleaned_data['selected_date']
        return date.strftime('%m-%d')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['photo']
