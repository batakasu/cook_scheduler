from django.views import generic
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from ..models import Recipe
from ..forms import RecipeIngredientFormSet
from ..permissions import accessible_recipes

class RecipeIngredientsUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Recipe
    pk_url_kwarg = 'recipe_pk'
    template_name = 'recipes/recipe_ingredients_update.html'
    context_object_name = 'recipe'
    fields = []

    def get_queryset(self):
        recipes = accessible_recipes(self.request.user).filter(user=self.request.user)
        return recipes
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if "recipe_ingredient_formset" not in context:
            data = self.request.POST if self.request.method == "POST" else None

            context["recipe_ingredient_formset"] = RecipeIngredientFormSet(
                data=data,
                instance=self.object
            )

        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context['recipe_ingredient_formset']

        if not formset.is_valid():
            return self.render_to_response(context)

        formset.save()

        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse('recipes:recipe_detail', kwargs={'pk': self.object.pk})