from django.views import generic
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from ..models import Recipe
from ..forms import RecipeForm, StepFormSet

class RecipeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Recipe
    template_name = 'recipes/recipe_update.html'
    context_object_name = 'recipe'
    form_class = RecipeForm
    
    def get_success_url(self):
        return reverse('recipes:recipe_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if "step_formset" not in context:
            data = self.request.POST if self.request.method == "POST" else None

            context["step_formset"] = StepFormSet(
                data=data,
                instance=self.object
            )

        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        step_formset = context['step_formset']

        if not step_formset.is_valid():
            return self.render_to_response(context)

        self.object = form.save()

        step_formset.instance = self.object
        step_formset.save()

        return HttpResponseRedirect(self.get_success_url())