from django.urls import path
from . import views


urlpatterns = [
    # path('', views.home, name="home")
    path('<int:year>/<int:month>/<int:day>', views.home, name="home"),
    path('', views.current_date),
    path('add_meeting', views.new_meeting, name="add_meeting"),
    path('edit/<int:pk>', views.edit_meeting, name='edit_meeting')
]