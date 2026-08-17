from django.shortcuts import render, redirect
from apps.tasks.forms import ProjectForm, TaskFormSet
from apps.tasks.models import Project, Membership

def add_project(request):
    if request.method == 'POST':
        project_form = ProjectForm(request.POST)

        if project_form.is_valid():
            if request.user.is_authenticated:
                project = project_form.save()

                Membership.objects.create(
                    project=project,
                    user=request.user
                )
            project = project_form.save()
            return redirect('core:home')
        
    else:
        project_form = ProjectForm()
        
    return render(request, 'tasks/add_project.html', {
        'project_form': project_form
    })