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

    cyclicals_regular = (('d', 'codziennie'), 
                        ('w', 'co tydzień'), 
                        ('m', 'co miesiąc'), 
                        ('y', 'co roku'),
                        ('h', 'dostosuj'))
    cyclicals_irregular = (('d', 'dni'),
                        ('w', 'tygodni'),
                        ('m', 'miesięcy'),
                        ('y', 'lat'))
                        # ('h', 'Wybierz konkretne dni tygodnia'))
    # cyclical_week_days = (('m', 'pn'),
    #                     ('t', 'wt'), 
    #                     ('w', 'śr'),
    #                     ('r', 'czw'), 
    #                     ('f', 'pt'),
    #                     ('s', 'so'),
    #                     ('n', 'nd'))

    cyclical = forms.BooleanField(initial=False, required=False)
    cyclical_regular = forms.ChoiceField(choices=cyclicals_regular, required=False)
    cyclical_number = forms.CharField(initial=1, required=False)
    cyclical_irregular = forms.ChoiceField(choices=cyclicals_irregular, required=False)
    # cyclical_week_days_how_often = cyclical_number = forms.CharField(initial=1, required=False)
    # cyclical_irregular_week_days = forms.MultipleChoiceField(choices=cyclical_week_days, required=False)

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

class NoteModelForm(BSModalModelForm):
    class Meta:
        model = Notes
        fields = ['text']

        labels = {"text": ("Wprowadź notatkę:")}