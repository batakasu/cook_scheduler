import json
from datetime import timedelta
from django.http import JsonResponse
from django.views import generic
from ..models import Project, Task, Membership
from ..permissions import accessible_projects, accessible_tasks, accessible_memberships
from datetime import datetime
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    pk_url_kwarg = 'project_pk'
    model = Project
    template_name = 'schedules/project_detail.html'
    context_object_name = 'project'

    def get_queryset(self):
        projects = accessible_projects(self.request.user)
        return projects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object

        members = project.members.all()
        members_data = []
        for member in members:
            if member.user:
                name = member.user.display_name or member.user.username
            else:
                name = member.guest_name

            members_data.append({
                'id': member.id,
                'content': name,
            })

        context['members_json'] = json.dumps(members_data)

        tasks = project.tasks.all()
        context['tasks'] = tasks
        tasks_data = []
        if project.scheduled_at:
            for t in tasks:
                start_time = project.scheduled_at + timedelta(minutes=t.start_offset)
                end_time = start_time + timedelta(minutes=t.duration)

                # idがあるならTrue、無いならFalse
                conflicting = bool(t.find_conflicting_tasks())

                tasks_data.append({
                'id': t.id,
                'content': t.title,
                'group' : t.membership_id,
                'start': start_time.isoformat(),
                'end': end_time.isoformat(),
                'conflicting': conflicting,
                'description': t.description,
                'duration': t.duration
            })

        context['tasks_json'] = json.dumps(tasks_data)
        return context

@login_required
def update_task(request):
    if request.method != 'POST':
        return JsonResponse({'success': False}, status=405)
    
    try:
        data = json.loads(request.body)
        task_id = data.get('id')
        start_str = data.get('start')
        end_str = data.get('end')
        membership_id = data.get('group')

        #時間のデータ取得
        if not start_str or not end_str:
            return JsonResponse({'success': False, 'error': '開始日時と終了日時を指定してください'}, status=400)

        new_start = datetime.fromisoformat(start_str.replace('Z', '+00:00'))
        new_end = datetime.fromisoformat(end_str.replace('Z', '+00:00'))

        # 作業時間が0分以下なら
        if new_end <= new_start:
            return JsonResponse({'success': False, 'error': '終了日時は開始日時より後にしてください'}, status=400)

        with transaction.atomic():
            task = accessible_tasks(request.user).select_related('project').get(pk=task_id)
            project = task.project

            if project.scheduled_at is None:
                return JsonResponse({'success': False,'error': '献立の開始日時が設定されていません'},status=400)
            
            duration = new_end - new_start
            start_offset = new_start - project.scheduled_at

            old_offset = task.start_offset

            task.duration = int(duration.total_seconds() // 60)
            task.start_offset = int(start_offset.total_seconds() // 60)
            task.membership = Membership.objects.get(pk=membership_id, project=project)

            task.save(update_fields=["duration", "start_offset", "membership"])

            if task.from_task is not None:
                first_task = task.find_first_task()
                move_time = task.start_offset - old_offset
                first_task.start_offset = first_task.start_offset + move_time
            else:
                first_task = task
            first_task.save(update_fields=['start_offset'])
            first_task.update_next_task_offsets()

            normalize_task_offsets(project) 

        return JsonResponse({'success': True})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

def normalize_task_offsets(project):
    first_task = project.tasks.order_by('start_offset').first()

    if first_task is None:
        return
    
    offset_minutes = first_task.start_offset

    if offset_minutes == 0:
        return
    

    #他のタスクのoff_setを調整
    other_tasks = Task.objects.filter(project=project)
    for t in other_tasks:
        t.start_offset -= offset_minutes
        t.save(update_fields=["start_offset"])

    project.scheduled_at += timedelta(minutes=offset_minutes)
    project.save(update_fields=["scheduled_at"])

@login_required
def add_new_task(request):
    if request.method != 'POST':
        return JsonResponse({'success': False}, status=405)
    
    try:
        data = json.loads(request.body)
        project_id = data.get('project_id')
        project = accessible_projects(request.user).get(id=project_id)
        start_str = data.get('start')

        if not start_str:
            return JsonResponse({'success': False, 'error': '開始日時を指定してください'}, status=400)

        start = datetime.fromisoformat(start_str.replace('Z', '+00:00'))
        offset = int((start - project.scheduled_at).total_seconds() // 60)

        # データベースに保存（長さは5分固定、オフセットはプロジェクト開始からの累計分）
        membership_obj = accessible_memberships(request.user).get(id=data.get('group'), project=project)
        Task.objects.create(
            project=project,
            title=data.get('content'),
            membership=membership_obj,
            duration=5,
            start_offset=offset
        )
        return JsonResponse({'success': True})
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@login_required
def copy_task(request):
    if request.method != 'POST':
        return JsonResponse({'success': False}, status=405)
    
    try:
        data = json.loads(request.body)
        task_id = data.get('task_id')

        original = accessible_tasks(request.user).get(pk=task_id)

        Task.objects.create(
            project=original.project,
            membership=original.membership,
            title=original.title,
            description=original.description,
            leave=original.leave,
            category=original.category,
            duration=original.duration,
            start_offset=original.start_offset,
            from_task=None,
        )
        return JsonResponse({'success': True})
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'success': False, 'error': str(e)}, status=400)