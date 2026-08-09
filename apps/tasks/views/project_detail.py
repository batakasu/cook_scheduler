import json
from datetime import timedelta
from django.http import JsonResponse
from django.views import generic
from apps.tasks.models import Project, Task
from datetime import datetime

class ProjectDetailView(generic.DetailView):
  model = Project
  template_name = 'tasks/project_detail.html'
  context_object_name = 'project'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    project = self.object
    tasks = project.tasks.all()
    context['tasks'] = tasks

    tasks_data = []
    if project.scheduled_at:
      current_time = project.scheduled_at
      for task in tasks:
        start_time = current_time + timedelta(minutes=task.start_offset)
        end_time = start_time + timedelta(minutes=task.duration)

        tasks_data.append({
            'id': task.id,
            'content': task.title,
            'start': start_time.isoformat(),
            'end': end_time.isoformat(),
        })
        current_time = end_time

    context['tasks_json'] = json.dumps(tasks_data)

    return context

def update_task_time(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            task_id = data.get('id')
            new_start_str = data.get('start')
            
            if new_start_str:
                task = Task.objects.get(id=task_id)
                project = task.project
                
                if project and project.scheduled_at:
                    # 1. 送られた開始時間をパースしてナイーブなdatetimeにする
                    new_start = datetime.fromisoformat(new_start_str.replace('Z', '+00:00'))
                    if project.scheduled_at.tzinfo is not None:
                        new_start = new_start.astimezone(project.scheduled_at.tzinfo)
                    start_naive = new_start.replace(tzinfo=None)
                    
                    # 2. 直前のタスクを取得する（順番が保証されている前提）
                    tasks = list(project.tasks.order_by('order'))
                    index = tasks.index(task)
                    
                    if index == 0:
                        project.scheduled_at = new_start
                        project.save()
                    else:
                        prev_task = tasks[index - 1]
                        prev_end_time = project.scheduled_at.replace(tzinfo=None)
                        for t in tasks[:index]:  # 直前までのタスクだけに絞る
                            prev_end_time += timedelta(minutes=t.start_offset + t.duration)
    
                        task.start_offset = int((start_naive - prev_end_time).total_seconds() // 60)
                        task.save()

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'success': False}, status=405)