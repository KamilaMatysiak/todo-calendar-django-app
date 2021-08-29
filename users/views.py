from bootstrap_modal_forms.generic import BSModalCreateView, BSModalLoginView
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

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


# def register(request):
#    if request.method == 'POST':
#        form = UserRegisterForm(request.POST)
#        if form.is_valid():
#            form.save()
# username = form.cleaned_data.get('username')
#            messages.success(request, f'Twoje konto zostało pomyślnie zarejestrowane!')
#            return redirect('login')
#    else:
#        form = UserRegisterForm()
#    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'users/profile.html')
