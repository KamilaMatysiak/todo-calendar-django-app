from django import forms
from django.forms import ModelForm
from .models import *


class TaskForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nowe zadanie'}))
    localization = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Lokalizacja'}), required=False)
    with_who = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Kontakty'}), required=False)
    date = forms.DateTimeField(widget=forms.DateTimeInput(format='%d-%m-%Y %H:%M',
                                                          attrs={'class': 'myDateClass',
                                                                 'placeholder': 'Data'}), required=False)

    class Meta:
        model = Task
        fields = '__all__'
