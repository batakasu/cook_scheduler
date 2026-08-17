from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('add/', views.add_project, name='add'),
    path('list/', views.list, name='list'),
    path('<int:project_pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('<int:project_pk>/tasks/<int:task_pk>/', views.TaskDetail.as_view(), name='task_detail'),
    path('update_task/', views.update_task, name='update_task'),
    path('add_new_task/', views.add_new_task, name='add_new_task'),
    path('delete/<int:task_pk>/', views.delete_task.as_view(), name='delete_task'),
]