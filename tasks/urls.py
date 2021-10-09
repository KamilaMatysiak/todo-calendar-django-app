from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.homepage, name="index"),
    path('home', views.index, name="vtodo"),
    path('task-list', views.task_list, name="list"),
    path('add_task', views.AddTaskView.as_view(), name="add_task"),
    path('add_category', views.AddCategoryView.as_view(), name="add_category"),
    path('update_task/<str:pk>/', views.EditTaskView.as_view(), name="update_task"),
    path('edit_cat/<str:pk>/', views.EditCategoryView.as_view(), name="edit_cat"),
    path('delete/<str:pk>/', views.DeleteTaskView.as_view(), name="delete"),
    path('delete_cat/<str:pk>', views.DeleteCategoryView.as_view(), name="delete_cat"),
    path('task-list/finish', views.finishTask, name="finish-task"),
    path('task-list/<str:pk>', views.categoryView, name="category"),
    path('test', views.test, name="test")
]