from django.views.generic import ListView
from django.db.models import Q
from ..models import Recipe

class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/recipe_list.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        qs1 = Recipe.objects.filter(user=self.request.user)
        qs2 = Recipe.objects.filter(is_public=True)

        recipes = qs1 | qs2
        return recipes.order_by('-created_at') # 新しい順（デフォルト）