from django.views import generic
from ..models import Recipe

class RecipeDetailView(generic.DetailView):
    model = Recipe
    template_name = 'recipes/recipe_detail.html'
    context_object_name = 'recipe'