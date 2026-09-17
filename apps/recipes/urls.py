from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.RecipeListView.as_view(), name='recipe_list'),
    path('recipe_create/', views.RecipeCreateView.as_view(), name='recipe_create'),
    path('recipe_detail/<int:pk>', views.RecipeDetailView.as_view(), name='recipe_detail'),
    path('recipe_update/<int:pk>', views.RecipeUpdateView.as_view(), name='recipe_update'),
]