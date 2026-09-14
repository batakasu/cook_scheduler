from django.views.generic import ListView
from ..models import Recipe

class RecipeListView(ListView):
    model = Recipe
    template_name = 'schedules/recipe_list.html'
    context_object_name = 'recipe_list'