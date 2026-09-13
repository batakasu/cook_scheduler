from .models import Project, Task, Membership
from apps.recipes.models import Recipe, Step
from django.db import transaction

def include_recipe(project, recipe, membership):
    with transaction.atomic():
        from_task = None
        start_at = 0
        if membership.project_id != project.id:
            membership = Membership.objects.filter(project=project).order_by("id").first()

        for s in recipe.steps.all():
            created_task = Task.objects.create(
                project = project,
                membership = membership,
                title = '未題',
                description = s.description,
                leave = s.leave,
                from_task = from_task,
                category = s.category,
                start_offset = start_at,
                duration = s.duration
            )
            from_task = created_task
            start_at += s.duration