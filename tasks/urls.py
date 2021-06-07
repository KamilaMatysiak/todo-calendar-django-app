from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="list"),
    path('home', views.homepage, name="index"),
    path('test-list', views.test_list, name="test"),
    path('update_task/<str:pk>/', views.updateTask, name="update_task"),
    path('delete/<str:pk>/', views.deleteTask, name="delete")
]