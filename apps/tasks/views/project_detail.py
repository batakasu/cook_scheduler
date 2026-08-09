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
                    # 1. JSから送られた日時をパース
                    new_start = datetime.fromisoformat(new_start_str.replace('Z', '+00:00'))
                    
                    # タイムゾーンを project.scheduled_at に合わせる
                    if project.scheduled_at.tzinfo is not None:
                        new_start = new_start.astimezone(project.scheduled_at.tzinfo)
                    else:
                        new_start = new_start.astimezone().replace(tzinfo=None)
                    
                    start_naive = new_start.replace(tzinfo=None)
                    
                    # 2. 【重要】このタスクの「直前の終了時刻（起点）」を計算する
                    # プロジェクトに属するタスクを順番に取得し、対象タスクの直前までの時間を積算する
                    current_time = project.scheduled_at.replace(tzinfo=None)
                    all_tasks = project.tasks.all() # ※リレーション名が異なる場合は合わせてください
                    
                    for t in all_tasks:
                        if t.id == task.id:
                            # ここが今回のタスクなので、ループを抜ける（current_time が直前の終了時刻になる）
                            break
                        # 自分より前のタスクの期間（duration）を足し合わせていく
                        # ※もし前のタスクも個別のoffsetを持っている等であればそれに合わせますが、
                        # 基本のロジックとしては duration 分進めます
                        current_time += timedelta(minutes=t.duration)
                    
                    # 3. 「直前の終了時刻」と「新しくドラッグされた開始時刻」の差分（分数）をオフセットとする
                    diff = start_naive - current_time
                    new_offset = int(diff.total_seconds() // 60)
                    
                    # 4. 保存
                    task.start_offset = new_offset
                    task.save()
                    print(f"Task {task_id} offset updated: base={current_time}, new_start={start_naive}, offset={new_offset}")

            return JsonResponse({'success': True})
            
        except Task.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Task not found'}, status=404)
        except Exception as e:
            print("SAVE ERROR:", str(e))
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

    return JsonResponse({'success': False, 'error': 'Invalid method'}, status=405)