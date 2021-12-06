from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.files.images import get_image_dimensions
from users.models import UserProfile
from bootstrap_modal_forms.forms import BSModalModelForm
from django.utils.translation import ugettext, ugettext_lazy as _
from bootstrap_datepicker_plus import DatePickerInput
from phonenumber_field.formfields import PhoneNumberField


class UserRegisterForm(PopRequestMixin, CreateUpdateAjaxMixin, UserCreationForm):
    password1 = forms.CharField(max_length=16, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Podaj hasło', 'data-toggle': 'password'}),
                                label="Hasło")
    password2 = forms.CharField(max_length=16, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Powtórz hasło'}),
                                label="Powtórz hasło")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Nazwa użytkownika'}),
            'email': forms.EmailInput(attrs={'placeholder': 'E-mail'}),
        }
        labels = {
            'username': ('Nazwa użytkownika'),
            'email': ('E-mail'),
        }
        help_texts = {
            'username': None
        }


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class UserProfileForm(BSModalModelForm):
    phonenumber = PhoneNumberField(label="Numer telefonu")

    class Meta:
        model = UserProfile
        fields = ['firstname', 'birthdate', 'phonenumber']
        labels = {
            'firstname': ('Imię i nazwisko'),
            'birthdate': ('Data urodzenia'),
            'phonenumber': ('Numer telefonu')
        }

        widgets = {
            'birthdate': DatePickerInput(format="%d-%m-%Y", options={"locale": "pl"}),
        }


class UserAvatarForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar']

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']

        try:
            w, h = get_image_dimensions(avatar)

            # validate dimensions
            max_width = max_height = 100
            if w > max_width or h > max_height:
                raise forms.ValidationError(
                    u'Please use an image that is '
                    '%s x %s pixels or smaller.' % (max_width, max_height))

            # validate content type
            main, sub = avatar.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                raise forms.ValidationError(u'Please use a JPEG, '
                                            'GIF or PNG image.')

            # validate file size
            if len(avatar) > (20 * 1024):
                raise forms.ValidationError(
                    u'Avatar file size may not exceed 20k.')

        except AttributeError:
            """
            Handles case when we are updating the user profile
            and do not supply a new avatar
            """
            pass

        return avatar
