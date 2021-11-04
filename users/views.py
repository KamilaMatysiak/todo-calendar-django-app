from bootstrap_modal_forms.generic import BSModalCreateView, BSModalLoginView, BSModalUpdateView, BSModalDeleteView
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.http import Http404, HttpResponse
from .models import UserProfile

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

@login_required
def change_password(request):
    if request.method == 'POST':
        print("post")
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, _('Your password was successfully updated!'))
            print("form-valid");
            return redirect('profile/')
        else:
            print("form not-valid")
            messages.error(request, _('Please correct the error below.'))
    else:
        print("not-post")
        form = PasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', {
        'form': form
    })

class DeleteUserView(BSModalDeleteView):
    template_name = 'users/delete_user.html'
    model = User
    success_message = "Usunięto konto"
    success_url = reverse_lazy('vtodo')

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(DeleteUserView, self).get_object()
        if not obj == self.request.user:
            raise Http404
        return obj



@login_required
def profile(request):
    return render(request, 'users/profile.html')


def username_ifunique(request, pk):
    try:
        user = get_object_or_404(get_user_model(), username=pk)
        responce = pk
    except Http404:
        responce = "ok"
    return HttpResponse(content={"message": responce})