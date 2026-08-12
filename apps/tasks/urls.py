from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('add/', views.add_project, name='add'),
    path('list/', views.list, name='list'),
    path('<int:project_pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('<int:project_pk>/tasks/<int:task_pk>/', views.TaskDetail.as_view(), name='task_detail'),
    path('update_task_time/', views.update_task_time, name='update_task_time'),
    path('add_new_task/', views.add_new_task, name='add_new_task')
]