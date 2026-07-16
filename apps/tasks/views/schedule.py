from django.shortcuts import render
from apps.tasks.models import Task

# Create your views here.
def schedule(request):
    tasks = Task.objects.all().order_by('id')
    return render(request, 'tasks/schedule.html', {'tasks': tasks})