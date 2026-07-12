from django.shortcuts import render
from .models import Task

# Create your views here.
def schedule_view(request):
    tasks = Task.objects.all().order_by('id')
    return render(request, 'tasks/schedule.html', {'tasks': tasks})