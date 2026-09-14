from django.views import generic
from django.urls import reverse
from django.shortcuts import get_object_or_404
from ..models import Recipe

class RecipeDetailView(generic.UpdateView):
    pk_url_kwarg = 'recipe_pk'
    model = Recipe
    template_name = 'recipes/recipe_detail.html'
    context_object_name = 'recipe'