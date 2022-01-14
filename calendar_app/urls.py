from django.urls import path
from . import views

urlpatterns = [

    path('day/<int:year>/<int:month>/<int:day>', views.home, name="home"),
    path('week/<int:year>/<int:month>/<int:day>', views.weekView, name="week"),
    path('month/<int:year>/<int:month>/<int:day>', views.monthView, name="month"),
    path('', views.current_date, name="date"),
    path('add_meeting', views.AddEventView.as_view(), name="add_meeting"),
    path('connect_task/<int:pk>', views.ConnectTaskView.as_view(), name="connect_task"),
    path('add_note/<int:meeting_pk>', views.AddNoteView.as_view(), name="add_note"),
    path('edit_note/<str:pk>/', views.EditNoteView.as_view(), name="edit_note"),
    path('edit_note/<str:pk>/delete_note', views.DeleteNoteView.as_view(), name="delete_note"),
    #path('retrieve_google_contacts', views.retrieve_google_contacts, name="retrieve_contacts"),
    path('import_google_calendar_data', views.import_google_calendar_api, name="import_calendar"),
    path('edit/<int:pk>', views.edit_meeting, name='edit_meeting'),
    path('delete/<int:pk>', views.DeleteEventView.as_view(), name="delete_meeting")
]
