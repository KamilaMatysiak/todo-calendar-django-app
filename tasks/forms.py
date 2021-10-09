from django import forms
#from django.forms import ModelForm
from .models import *
from bootstrap_modal_forms.forms import BSModalModelForm
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput
from django.contrib.auth.models import User

class TaskModelForm(BSModalModelForm):
    
    with_who = forms.CharField(required=False, label="Kontakty")
    localization = forms.CharField(required=False, label="Lokalizacja")
    
    class Meta:
        model = Task
        fields = ['title', 'localization', 'with_who', 'date', 'time', 'priority']
        widgets = {
            'date': DatePickerInput(format="%d-%m-%Y", options={"locale": "pl"}),
            'time': TimePickerInput()
        }
        labels = {
            'title': ('Nazwa zadania'),
            'date': ('Data'),
            'time': ('Czas'),
            'priority': ('Priorytet'),
        }

class CategoryModelForm(BSModalModelForm):

    class Meta:
        model = Category
        fields = ['title']
        labels = {'title': ('Nazwa kategorii:')}