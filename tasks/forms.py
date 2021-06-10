from django import forms
from django.forms import ModelForm
from .models import *


class TaskForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Add new task...'}))
    localization = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Set localization'}), required=False)
    with_who = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'With who?'}), required=False)

    class Meta:
        model = Task
        fields = '__all__'
