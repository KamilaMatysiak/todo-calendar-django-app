from bootstrap_modal_forms.generic import BSModalCreateView, BSModalLoginView
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _

from .forms import UserRegisterForm, CustomAuthenticationForm


class SignUpView(BSModalCreateView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_message = 'Zarejestrowano. Możesz się zalogować'
    success_url = reverse_lazy('index')


class LoginView(BSModalLoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'users/login.html'
    success_message = 'Zalogowano'
    success_url = reverse_lazy('index')


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, _('Your password was successfully updated!'))
            return redirect('profile/')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', {
        'form': form
    })


@login_required
def profile(request):
    return render(request, 'users/profile.html')
