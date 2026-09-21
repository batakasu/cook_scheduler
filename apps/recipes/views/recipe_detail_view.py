from django.views import generic
from ..models import Recipe
from ..permissions import accessible_recipes
from django.contrib.auth.mixins import LoginRequiredMixin

class RecipeDetailView(LoginRequiredMixin, generic.DetailView):
    model = Recipe
    template_name = 'recipes/recipe_detail.html'
    context_object_name = 'recipe'
    
    def get_queryset(self):
        recipes = accessible_recipes(self.request.user)
        return recipes