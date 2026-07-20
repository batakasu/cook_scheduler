from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('add/', views.add_project, name='add'),
    path('list/', views.list, name='list'),
    path('<int:pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
]