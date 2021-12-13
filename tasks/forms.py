from django import forms
from django.contrib.sites.models import Site
from django.urls import reverse_lazy

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

import requests as api_reqs

domain_local = 'http://127.0.0.1:8000'
domain_aws = 'https://v-todo.com'


class TaskModelForm(BSModalModelForm):

    def __init__(self, user, *args, **kwargs):
        super(TaskModelForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(user=user)

    with_who = forms.CharField(required=False, widget=forms.Select(choices=(),attrs={"name": "contacts[]", "class": "js-example-basic-multiple field-sel", "style": "width: 100%", "multiple": "multiple"}), label="Kontakty")
    localization = forms.CharField(required=False, label="Lokalizacja")
    for_who = forms.CharField(required=False, label="Zlecenie", validators=[temporary_user_validation])

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