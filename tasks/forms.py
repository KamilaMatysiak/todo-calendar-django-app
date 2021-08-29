from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User


class TaskForm(forms.ModelForm):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nowe zadanie'}))
    localization = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Lokalizacja'}), required=False)
    with_who = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Kontakty'}), required=False)
    date = forms.DateField(widget=forms.DateInput(format='%d-%m-%Y',
                                                          attrs={'class': 'myDateClass',
                                                                 'placeholder': 'Data'}), required=False)

    class Meta:
        model = Task
        fields = '__all__'
