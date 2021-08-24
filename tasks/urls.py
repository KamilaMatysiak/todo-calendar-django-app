from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="vtodo"),
    path('home', views.homepage, name="index"),
    path('task-list', views.task_list, name="list"),
    path('add_task', views.addTask, name="add_task"),
    path('update_task/<str:pk>/', views.updateTask, name="update_task"),
    path('delete/<str:pk>/', views.deleteTask, name="delete"),
]