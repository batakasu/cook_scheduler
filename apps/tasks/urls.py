from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('add/', views.add_project, name='add'),
]