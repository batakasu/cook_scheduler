from django.shortcuts import render, redirect
from .models import Recipe
from .forms import RecipeForm, StepFormSet

# Create your views here.
def list_view(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes/list.html', {'recipes': recipes})

def add_recipe(request):
    if request.method == "POST":
        form = RecipeForm(request.POST)
        formset = StepFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            recipe = form.save()
            formset.instance = recipe
            formset.save()
            return redirect('recipes:list')
    else:
        form = RecipeForm()
        formset = StepFormSet()
    
    return render(request, 'recipes/add_recipe.html', {'form': form, 'formset': formset})