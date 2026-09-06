from django.urls import path
from . import views

app_name = 'schedules'

urlpatterns = [
    path('<int:project_pk>/members/', views.MembershipListView.as_view(), name='membership_list'),
    path('create/', views.ProjectCreateView.as_view(), name='project_create'),
    path('list/', views.ProjectListView.as_view(), name='project_list'),
    path('<int:project_pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('<int:project_pk>/tasks/<int:task_pk>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('<int:project_pk>/tool_list/', views.ToolListView.as_view(), name='tool_list'),
    path('<int:project_pk>/tools/<int:tool_pk>/', views.ToolDetailView.as_view(), name='tool_detail'),
    path('update_task/', views.update_task, name='update_task'),
    path('add_new_task/', views.add_new_task, name='add_new_task'),
    path('delete/<int:task_pk>/', views.TaskDeleteView.as_view(), name='delete_task'),
]