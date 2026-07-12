from django.shortcuts import render
from .models import Recipe

# Create your views here.
def list_view(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes/list.html', {'recipes': recipes})
