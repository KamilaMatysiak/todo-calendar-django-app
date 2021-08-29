from django import forms
from django.forms import ModelForm
from .models import *
from bootstrap_modal_forms.forms import BSModalModelForm
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput


class EventModelForm(BSModalModelForm):
    description = forms.CharField(required=False, label="Opis")

    class Meta:
        model = Meeting
        fields = ['title', 'description', 'date_start', 'time_start', 'time_end', 'date_end']
        widgets = {
            'date_start': DatePickerInput(format="%d-%m-%Y", options={"locale": "pl"}),
            'date_end': DatePickerInput(format="%d-%m-%Y", options={"locale": "pl"}),
            'time_start': TimePickerInput(),
            'time_end': TimePickerInput(),
        }
        labels = {
            'title': ('Nazwa spotkania'),
            'date_start': ('Data rozpoczęcia'),
            'time_start': ('Rozpoczęcie'),
            'time_end': ('Zakończenie'),
            'date_end': ('Data zakończenia')
        }
