from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.list, name='list'),
    path('add/', views.add_recipe, name='add'),
]