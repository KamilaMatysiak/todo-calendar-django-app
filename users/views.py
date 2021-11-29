import datetime

from allauth.socialaccount.models import SocialAccount, SocialToken
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
from django.http import Http404, JsonResponse
from .models import UserProfile
from .forms import UserRegisterForm, CustomAuthenticationForm, UserProfileForm
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from allauth.socialaccount.models import SocialToken
import requests as api_reqs


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


class EditUserView(BSModalUpdateView):
    model = UserProfile
    template_name = 'users/edit_profile.html'
    form_class = UserProfileForm
    success_message = "Pomyślnie zedytowano konto"
    success_url = reverse_lazy('profile')


def build_credentials(token):
    return Credentials(token=token.token,
                       refresh_token=token.token_secret,
                       client_id=token.app.client_id,
                       client_secret=token.app.secret,
                       )


def construct_people_service(user):
    social_token = SocialToken.objects.get(account__user=user)
    creds = build_credentials(social_token)
    return build('people', 'v1', credentials=creds)


@login_required
def profile(request):

    userProfile, costam = UserProfile.objects.get_or_create(user=request.user,
                                                            firstname=request.user.first_name + ' ' + request.user.last_name)
    print(userProfile)
    print(costam)
    if not costam:

        google_user = SocialAccount.objects.filter(user=request.user).first()
        if google_user:
            service = construct_people_service(request.user)
            res = service.people().get(resourceName="people/me", personFields='names,birthdays,phoneNumbers').execute()
            print('res: ', res)
            if res.get('birthdays', None):
                new_birthdate = datetime.date(**res['birthdays'][0]['date'])
                print(new_birthdate)
                userProfile.birthdate = new_birthdate
                userProfile.save()
            if res.get('phoneNumbers', None):
                print(res['phoneNumbers'])

    return render(request, 'users/profile.html', {'userProfile': userProfile})


def username_ifunique(request, pk):
    response = {'message': ''}
    try:
        user = get_object_or_404(get_user_model(), username=pk)
        response['message'] = 'error'
    except Http404:
        response['message'] = "ok"
    return JsonResponse(response)


@login_required
def retrieve_google_contacts(request):
    import xml.etree.ElementTree as ET

    user = request.user
    try:
        social_token = SocialToken.objects.get(account__user=user)

        url = 'https://www.google.com/m8/feeds/contacts/default/full' + '?access_token=' + social_token.token + '&max-results=100'
        data = api_reqs.get(url, headers={
            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.30 (KHTML, like Gecko) Ubuntu/11.04 Chromium/12.0.742.112 Chrome/12.0.742.112 Safari/534.30"})
        contacts_xml = ET.fromstring(data.text)
        result = []

        for entry in contacts_xml.findall('{http://www.w3.org/2005/Atom}entry'):
            for address in entry.findall('{http://schemas.google.com/g/2005}email'):
                email = address.attrib.get('address')
                result.append(email)
        response = {'msg': 'success',
                    'data': result}

    except Exception as e:
        print("Got next error when tried to get google contacts: ", e)
        response = {'msg': 'error',
                    'data': e}
    return JsonResponse(response)


@login_required
def retrieve_google_contacts_via_service(request):
    service = construct_people_service(request.user)
    res = service.people().connections().list(resourceName="people/me", pageSize=10,
                                              personFields='names,birthdays').execute()
    print(res)
    print(res.keys())
    print(f"{ res.get('nextPageToken', []) =  }")
    print(f"{ res.get('totalPeople', []) =  }")
    print(f"{ res.get('totalItems', []) =  }")
    connections = res.get('connections', [])

    for person in connections:
        print(person)
        names = person.get('names', [])
        if names:
            name = names[0].get('displayName')
            print(name)
        print('-'*20)
    return JsonResponse(connections, safe=False)
