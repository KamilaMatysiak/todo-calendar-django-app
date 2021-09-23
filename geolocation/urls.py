from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.urls import path, include
from . import views

from .views import send_push, home
from django.views.generic import TemplateView

urlpatterns = [
    url('^(?P<lat>\d+\.?\d*)_(?P<lon>\d+\.?\d*)$', views.location, name="location-2"),
    path('', views.start, name="location"),
    path('send_push', send_push, name="send"),
    path('webpush/', include('webpush.urls')),
    path('', home),
    path('serviceworker.js', TemplateView.as_view(template_name='serviceworker.js', content_type='application/x'
                                                                                                  '-javascript')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
