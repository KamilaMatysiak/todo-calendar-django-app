from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.urls import path, include
from . import views
from django.views.generic import TemplateView
#from tasks.views import send_push

urlpatterns = [
    path('', views.location, name="location"),
    path('<str:pk>', views.location, name="location"),
    #path('send_push', send_push, name="send_push"),
    path('webpush/', include('webpush.urls')),
    path('serviceworker.js', TemplateView.as_view(template_name='serviceworker.js', content_type='application/x'
                                                                                                  '-javascript')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
