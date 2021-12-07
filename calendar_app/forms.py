from django import forms
from django.forms import ModelForm
from .models import *
from bootstrap_modal_forms.forms import BSModalModelForm
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput
from datetime import *


class EventModelForm(BSModalModelForm):
    description = forms.CharField(required=False, label="Opis")
    today = datetime.now().strftime("%d-%m-%Y")

    COLORS = [('blue', 'blue'),
            ('orange', 'orange'),
            ('red', 'red'),
            ('purple', 'purple'),
            ('green', 'green')]

    color = forms.CharField(label="Kolor", widget=forms.RadioSelect(choices=COLORS), initial="blue")
    with_who = forms.CharField(required=False, label="Kontakty")
    localization = forms.CharField(required=False, label="Lokalizacja")

    class Meta:
        model = Meeting
        fields = ['color', 'title', 'description', 'localization', 'with_who', 'date_start', 'time_start', 'time_end', 'date_end']
        widgets = {
            # 'x': DatePickerInput(format="%d-%m-%Y", options={"locale": "pl"}),
            'date_start': DatePickerInput(format="%d-%m-%Y", options={"locale": "pl", "useCurrent": False}),
            'date_end': DatePickerInput(format="%d-%m-%Y", options={"locale": "pl", "useCurrent": False}),
            'time_end': TimePickerInput(),
            'time_start': TimePickerInput(),

        }
        labels = {
            'title': ('Nazwa spotkania'),
            'date_start': ('Data rozpoczęcia'),
            'time_start': ('Godzina rozpoczęcie'),
            'time_end': ('Godzina zakończenia'),
            'date_end': ('Data zakończenia')
        }
