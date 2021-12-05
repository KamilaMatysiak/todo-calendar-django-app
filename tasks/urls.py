from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.homepage, name="index"),
    path('home', views.index, name="vtodo"),
    path('task-list', views.task_list, name="list"),
    path('add_task', views.AddTaskView.as_view(), name="add_task"),
    path('add_category', views.AddCategoryView.as_view(), name="add_category"),
    path('delegate', views.delegateView, name="delegate"),
    path('update_task/<str:pk>/', views.EditTaskView.as_view(), name="update_task"),
    path('edit_cat/<str:pk>/', views.EditCategoryView.as_view(), name="edit_cat"),
    path('delete/<str:pk>/', views.DeleteTaskView.as_view(), name="delete"),
    path('delete_cat/<str:pk>', views.DeleteCategoryView.as_view(), name="delete_cat"),
    path('task-list/finish', views.finishTask, name="finish-task"),
    path('home/<str:pk>/reject', views.refuse_task, name='reject'),
    path('home/<str:pk>/confirm', views.accept_task, name='confirm'),
    path('send_push', views.send_push),
    path('task-list/<str:pk>', views.categoryView, name="category"),
    path('test', views.test, name="test"),
    path('serviceworker.js', TemplateView.as_view(template_name='serviceworker.js', content_type='application/x'
                                                                                                  '-javascript')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
