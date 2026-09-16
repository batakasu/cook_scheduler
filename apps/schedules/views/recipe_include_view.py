from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from ..services import include_recipe
from ..models import Project, Membership
from apps.recipes.models import Recipe

class RecipeIncludeView(LoginRequiredMixin, View):
    def get(self, request, project_pk):
        project = get_object_or_404(
            Project,
            pk = project_pk
        )

        context = {
            'project': project,
            'recipes': Recipe.objects.all(),
        }

        return render(request, 'schedules/recipe_include.html', context)

    def post(self, request, project_pk):
        project = get_object_or_404(
            Project,
            pk=project_pk
        )
        recipe = get_object_or_404(
            Recipe,
            pk=request.POST.get('recipe_pk')
        )
        membership = get_object_or_404(
            Membership,
            project=project,
            user=request.user
        )

        include_recipe(
            project,
            recipe,
            membership
        )

        return redirect('schedules:project_detail', project_pk=project.pk)