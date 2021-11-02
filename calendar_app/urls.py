from django.urls import path
from . import views

urlpatterns = [

    path('<int:year>/<int:month>/<int:day>', views.home, name="home"),
    path('2020/6/12', views.home, name="home_empty"),
    path('', views.current_date, name="date"),
    path('add_meeting', views.AddEventView.as_view(), name="add_meeting"),
    path('edit/<int:pk>', views.edit_meeting, name='edit_meeting'),
    path('delete/<int:pk>', views.DeleteEventView.as_view(), name="delete_meeting")
]
