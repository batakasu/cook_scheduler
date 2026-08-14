import json
from datetime import timedelta
from django.http import JsonResponse
from django.views import generic
from apps.tasks.models import Project, Task, Membership
from datetime import datetime
from zoneinfo import ZoneInfo

class ProjectDetailView(generic.DetailView):
  pk_url_kwarg = 'project_pk'
  model = Project
  template_name = 'tasks/project_detail.html'
  context_object_name = 'project'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    project = self.object

    members = project.members.all()
    members_data = []
    for member in members:
        members_data.append({
            'id': member.id,
            'content': member.user.username if member.user else member.guest_name,
        })

    context['members_json'] = json.dumps(members_data)


    tasks = project.tasks.all()
    context['tasks'] = tasks
    tasks_data = []
    if project.scheduled_at:
      for task in tasks:
        start_time = project.scheduled_at + timedelta(minutes=task.start_offset)
        end_time = start_time + timedelta(minutes=task.duration)

        tasks_data.append({
            'id': task.id,
            'content': task.title,
            'group' : task.membership_id,
            'start': start_time.isoformat(),
            'end': end_time.isoformat(),
        })

    context['tasks_json'] = json.dumps(tasks_data)

    return context

def update_task_time(request):
    if request.method != 'POST':
        return JsonResponse({'success': False}, status=405)

    try:
        data = json.loads(request.body)
        task_id = data.get('id')
        new_start_str = data.get('start')

        if not new_start_str:
            return JsonResponse({'success': False, 'error': 'Start time is missing'}, status=400)

        task = Task.objects.get(id=task_id)
        project = task.project

        if not project or not project.scheduled_at:
            return JsonResponse({'success': False, 'error': 'Project schedule not found'}, status=400)

        new_start = datetime.fromisoformat(new_start_str.replace('Z', '+00:00'))
        if project.scheduled_at.tzinfo is not None:
            new_start = new_start.astimezone(project.scheduled_at.tzinfo)

        start_naive = new_start.replace(tzinfo=None)
        proj_start_naive = project.scheduled_at.replace(tzinfo=None)

        new_offset = int((start_naive - proj_start_naive).total_seconds() // 60)
        if new_offset < 0:
            new_offset = 0

        task.start_offset = new_offset
        task.save()
        return JsonResponse({'success': True})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

def add_new_task(request):
    if request.method != 'POST':
        return JsonResponse({'success': False}, status=405)
    
    try:
        data = json.loads(request.body)
        project_id = data.get('project_id')
        project = Project.objects.get(id=project_id)

        # 既存のタスクの中から、最後のタスクの終了位置（start_offset + duration）を計算
        last_task = project.tasks.order_by('order').last()
        if not last_task:
            start_offset = 0  # 最初のタスクならオフセット0
        else:
            start_offset = last_task.start_offset + last_task.duration

        # データベースに保存（長さは5分固定、オフセットはプロジェクト開始からの累計分）
        membership_obj = Membership.objects.get(id=data.get('group'))
        Task.objects.create(
            project=project,
            title=data.get('content'),
            membership=membership_obj,
            duration=5,
            start_offset=start_offset,
            order=project.tasks.count()
        )
        return JsonResponse({'success': True})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
