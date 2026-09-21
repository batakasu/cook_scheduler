from .models import Project, Task

def accessible_projects(user):
    return Project.objects.filter(
        members__user=user
    )

def accessible_tasks(user):
    return Task.objects.filter(
        project__members__user=user
    )