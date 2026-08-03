from django.shortcuts import render
from apps.tasks.models import Project

def list(request):
    sort_type = request.GET.get('sort', 'new')

    if sort_type == 'old':
        projects = Project.objects.order_by('scheduled_at')  # 古い順
    elif sort_type == 'title':
        projects = Project.objects.order_by('title')         # タイトル順
    else:
        projects = Project.objects.order_by('-scheduled_at') # 新しい順（デフォルト）

    context = {
        'projects': projects,
        'current_sort': sort_type,
    }
    return render(request, 'tasks/list.html', context)