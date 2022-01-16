from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.homepage, name="index"),
    path('home', views.index, name="vtodo"),
    path('task-list/finish', views.finishTask, name="finish-task"),
    path('task-list', views.task_list, name="list"),
    path('task-list/<str:pk>', views.task_list, name="list"),
    path('add_task', views.AddTaskView.as_view(), name="add_task"),
    path('add_category', views.AddCategoryView.as_view(), name="add_category"),
    path('delegate', views.delegateView, name="delegate"),
    path('update_task/<str:pk>/', views.EditTaskView.as_view(), name="update_task"),
    path('edit_cat/<str:pk>/', views.EditCategoryView.as_view(), name="edit_cat"),
    path('delete/<str:pk>/', views.DeleteTaskView.as_view(), name="delete"),
    path('delete_cat/<str:pk>', views.DeleteCategoryView.as_view(), name="delete_cat"),
    path('terms_of_service/', views.terms_of_service, name="terms_of_service"),
    path('user_manual/', views.user_manual, name="user_manual"),
    path('user_manual/pwa', views.pwa_manual, name="pwa_manual"),
    path('home/<str:pk>/reject', views.refuse_task, name='reject'),
    path('home/<str:pk>/confirm', views.accept_task, name='confirm'),
    path('send_push', views.send_push, name='send_push'),
    path('home/notification/<str:pk>/reject', views.reject_notification, name='reject_notification'),
    path('home/notification/<str:pk>/confirm', views.accept_notification, name='accept_notification'),
    path('category/<str:pk>', views.categoryView, name="category"),
    path('archive', views.archiveView, name="archive"),
    path('test', views.test, name="test"),
    path('serviceworker.js', TemplateView.as_view(template_name='serviceworker.js', content_type='application/x'
                                                                                                  '-javascript')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
