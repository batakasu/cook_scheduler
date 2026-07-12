from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('schedule/', views.schedule_view, name='schedule'),
]