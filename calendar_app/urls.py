from django.urls import path
from . import views


urlpatterns = [
    # path('', views.home, name="home")
    path('<int:year>/<int:month>/<int:day>', views.home, name="home"),
    path('', views.current_date)
]