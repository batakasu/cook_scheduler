from django.shortcuts import render
from apps.tasks.models import Project

def list(request):# ① URLから 'sort' というパラメータを受け取る（デフォルトは 'new'）
    sort_type = request.GET.get('sort', 'new')

    # ② 選択された条件に合わせて order_by を切り替える
    if sort_type == 'old':
        projects = Project.objects.order_by('scheduled_at')  # 古い順
    elif sort_type == 'title':
        projects = Project.objects.order_by('title')         # タイトル順
    else:
        projects = Project.objects.order_by('-scheduled_at') # 新しい順（デフォルト）

    # ③ HTMLにデータと「今どれが選ばれているか」を渡す
    context = {
        'projects': projects,
        'current_sort': sort_type,
    }
    return render(request, 'tasks/list.html', context)