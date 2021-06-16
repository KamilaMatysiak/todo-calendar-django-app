from django import forms
from django.forms import ModelForm
from .models import *


class MeetingForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'New task'}))
    time_start = forms.TimeField(widget=forms.TimeInput(format='%H:%M', attrs={'placeholder': '12:33 '}))
    time_end = forms.TimeField(widget=forms.TimeInput(format='%H:%M', attrs={'placeholder': '17:18'}))

    class Meta:
        model = Meeting
        fields = '__all__'