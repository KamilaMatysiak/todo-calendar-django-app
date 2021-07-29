from django import forms
from django.forms import ModelForm
from .models import *


class TaskForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nowe zadanie'}))
    localization = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Lokalizacja'}), required=False)
    with_who = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Kontakty'}), required=False)
    date = forms.DateField(widget=forms.DateInput(format=['%d-%m-%Y', '%d-%m-%y', '%d.%m.%Y', '%d.%m.%Y'],
                                                          attrs={'class': 'myDateClass',
                                                                 'placeholder': 'Data'}), required=False)

    class Meta:
        model = Task
        fields = '__all__'
