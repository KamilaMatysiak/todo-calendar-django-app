from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views

from .views import send_push, home
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.location, name="location"),
    path('send_push', send_push, name="send"),
    path('webpush/', include('webpush.urls')),
    path('', home),
    path('serviceworker.js', TemplateView.as_view(template_name='serviceworker.js', content_type='application/x'
                                                                                                  '-javascript')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
