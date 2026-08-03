from django.shortcuts import render
from apps.tasks.models import Project

def list(request):
    projects = Project.objects.order_by('-scheduled_at')
    return render(request, 'tasks/list.html', {'projects': projects})