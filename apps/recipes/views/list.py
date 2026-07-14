from django.shortcuts import render
from apps.recipes.models import Recipe

def list(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes/list.html', {'recipes': recipes})
