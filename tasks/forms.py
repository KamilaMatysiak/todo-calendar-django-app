from django import forms
#from django.forms import ModelForm
from .models import *
from bootstrap_modal_forms.forms import BSModalModelForm
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def temporary_user_validation(usernamw):
    users = User.objects.filter(username=usernamw)
    if len(users) == 0:
        raise ValidationError(
            "Nie ma takiego użytkownika!"
        )


class TaskModelForm(BSModalModelForm):

    def __init__(self, user, *args, **kwargs):
        super(TaskModelForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(user=user)

    with_who = forms.CharField(required=False, label="Kontakty")
    localization = forms.CharField(required=False, label="Lokalizacja")
    for_who = forms.CharField(required=False, label="Zlecenie", validators=[temporary_user_validation])
    
    cyclicals_regular = (('d', 'codziennie'), 
                        ('w', 'co tydzień'), 
                        ('m', 'co miesiąc'), 
                        ('y', 'co roku'),
                        ('h', 'dostosuj'))
    cyclicals_irregular = (('d', 'dni'),
                        ('w', 'tygodni'),
                        ('m', 'miesięcy'),
                        ('y', 'lat'))

    cyclical = forms.BooleanField(initial=False, required=False)
    cyclical_regular = forms.ChoiceField(choices=cyclicals_regular, required=False)
    cyclical_number = forms.CharField(initial=1, required=False)
    cyclical_irregular = forms.ChoiceField(choices=cyclicals_irregular, required=False)
    class Meta:
        model = Task
        fields = ['title', 'localization', 'with_who', 'date', 'time', 'priority', 'category']
        widgets = {
            'date': DatePickerInput(format="%d-%m-%Y", options={"locale": "pl"}),
            'time': TimePickerInput()
        }
        labels = {
            'title': ('Nazwa zadania'),
            'date': ('Data'),
            'time': ('Czas'),
            'priority': ('Priorytet'),
            'category': ('Kategoria'),
        }

    

class CategoryModelForm(BSModalModelForm):

    class Meta:
        model = Category
        fields = ['title']
        labels = {'title': ('Nazwa kategorii:')}