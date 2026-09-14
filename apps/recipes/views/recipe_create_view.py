from ..forms import RecipeForm
from ..models import Recipe
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_create.html'
    success_url = reverse_lazy('recipes/recipe_list')