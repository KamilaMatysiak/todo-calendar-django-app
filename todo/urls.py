"""todo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pwa.urls')),
    path('register/', user_views.SignUpView.as_view(), name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('edit_profile/<str:pk>/', user_views.EditUserView.as_view(), name="edit_profile"),
    path('check_username/<str:pk>', user_views.username_ifunique, name='check-username'),
    path('change_password', user_views.change_password, name="change"),
    path('delete_account/<str:pk>', user_views.DeleteUserView.as_view(), name="deleteac"),
    path('retrieve_google_contacts', user_views.retrieve_google_contacts, name="retrieve_contacts"),
    path('retrieve_contacts_alternate', user_views.retrieve_google_contacts_via_service,
         name="retrieve_contacts_alternate"),
    path('avatar/', include('avatar.urls')),
    path('login/', user_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('', include('tasks.urls')),
    # url('', include('social_django.urls', namespace='social')),
    path('', include('allauth.urls')),
    path('location/', include('geolocation.urls')),
    path('calendar/', include('calendar_app.urls')),
    url(r'^webpush/', include('webpush.urls')),
    url(r'^health/', views.health, name='health'),
    url(r'^ht/', include('health_check.urls')),

    path('serviceworker.js', TemplateView.as_view(template_name='serviceworker.js',
                    content_type='application/javascript'), name='serviceworker.js'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)\
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
