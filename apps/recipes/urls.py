from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.list, name='list'),
    path('recipe_create/', views.RecipeCreateView.as_view(), name='recipe_create'),
]