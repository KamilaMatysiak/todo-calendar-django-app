from django import forms
from django.forms import ModelForm, ModelMultipleChoiceField
from .models import *
from bootstrap_modal_forms.forms import BSModalModelForm
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput
from datetime import *
from tasks.models import Task



class EventModelForm(BSModalModelForm):
    description = forms.CharField(required=False, label="Opis")
    today = datetime.now().strftime("%d-%m-%Y")

    COLORS = [('blue', 'blue'),
            ('orange', 'orange'),
            ('red', 'red'),
            ('purple', 'purple'),
            ('green', 'green')]

    color = forms.CharField(label="Kolor", widget=forms.RadioSelect(choices=COLORS), initial="blue")

    class Meta:
        model = Meeting
        fields = ['color', 'title', 'description', 'date_start', 'time_start', 'time_end', 'date_end']
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

class ConnectTaskForm(BSModalModelForm):

    def __init__(self, user, *args, **kwargs):
        super(ConnectTaskForm, self).__init__(*args, **kwargs)
        self.fields['tasks'].queryset = Task.objects.filter(user=user)
        #self.fields['tasks'].initial = Task.objects.filter(meeting=self.object)

    tasks = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple )

    class Meta:
        model = Meeting
        fields = ['tasks']