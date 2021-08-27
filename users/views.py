from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm


def register(request):
    """
    Uses form to create new user account.
    Args:
        request: request to return .html file

    Returns: .html file of registration panel

    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data.get('username')
            messages.success(request, f'Twoje konto zostało pomyślnie zarejestrowane!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    """
    Show user profile.
    Args:
        request: request to return .html file.

    Returns: .html file of user's profile.

    """
    return render(request, 'users/profile.html')
