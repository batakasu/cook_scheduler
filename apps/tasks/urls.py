from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('schedule/', views.schedule, name='schedule'),
    path('create/', views.TaskCreate.as_view(), name='task_create'),
]