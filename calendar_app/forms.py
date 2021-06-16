from django import forms
from django.forms import ModelForm
from .models import *


class MeetingForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Add new task...'}))
    time_start = forms.TimeField(widget=forms.TimeInput(format='%H:%M', attrs={'placeholder': 'Add new task...'}))
    time_end = forms.TimeField(widget=forms.TimeInput(format='%H:%M', attrs={'placeholder': 'Add new task...'}))

    class Meta:
        model = Meeting
        fields = '__all__'