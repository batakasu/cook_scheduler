from django.shortcuts import render, redirect
from apps.tasks.forms import ProjectForm, TaskFormSet
from apps.tasks.models import Project, Task

def add_project(request):
    if request.method == 'POST':
        project_form = ProjectForm(request.POST)
        task_formset = TaskFormSet(request.POST)

        if project_form.is_valid() and task_formset.is_valid():
            project = project_form.save()
            task_formset.instance = project
            task_formset.save()
            return redirect('core:home')
    else:
        project_form = ProjectForm()
        task_formset = TaskFormSet()
        
    return render(request, 'tasks/add_project.html', {
        'project_form': project_form,
        'task_formset': task_formset
    })