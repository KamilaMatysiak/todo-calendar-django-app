from django import forms
from django.forms import ModelForm
from .models import *


class MeetingForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nowe zadanie'}))
    time_start = forms.TimeField(input_formats=['%H:%M'], widget=forms.TimeInput(format='%H:%M', attrs={'placeholder': 'gg:mm'}))
    time_end = forms.TimeField(input_formats=['%H:%M'], widget=forms.TimeInput(format='%H:%M', attrs={'placeholder': 'gg:mm'}))

    class Meta:
        model = Meeting
        fields = '__all__'