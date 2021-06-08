from django.urls import path
from . import views


urlpatterns = [
    # path('', views.home, name="home")
    path('<int:year>/<int:month>', views.home, name="home"),
    path('', views.current_date)
]