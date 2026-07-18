from django.shortcuts import render
from apps.tasks.models import Project

def list(request):
    projects = Project.objects.all()
    return render(request, 'tasks/list.html', {'projects': projects})