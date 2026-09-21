from django.views.generic import ListView
from ..models import Recipe
from ..permissions import accessible_recipes

class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/recipe_list.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        recipes = accessible_recipes(self.request.user)
        return recipes.order_by('-created_at') # 新しい順（デフォルト）