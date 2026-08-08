import json
from django.views import generic
from apps.tasks.models import Project
from datetime import timedelta

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