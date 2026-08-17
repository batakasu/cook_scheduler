from django.shortcuts import render
from apps.tasks.models import Project

def list(request):
    sort_type = request.GET.get('sort', 'new')

    base_projects = Project.objects.filter(members__user=request.user)

    if sort_type == 'old':
        projects = base_projects.order_by('scheduled_at')  # 古い順
    elif sort_type == 'title':
        projects = base_projects.order_by('title')         # タイトル順
    else:
        projects = base_projects.order_by('-scheduled_at') # 新しい順（デフォルト）

    context = {
        'projects': projects,
        'current_sort': sort_type,
    }
    return render(request, 'tasks/list.html', context)