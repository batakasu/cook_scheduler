from django.views import generic
from django.urls import reverse
from apps.tasks.models import Task
from apps.tasks.forms import TaskForm

class TaskDetail(generic.UpdateView):
    pk_url_kwarg = 'task_pk'
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'
    form_class = TaskForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_form'] = context['form']
        return context
    
    def get_success_url(self):
        project_pk = self.kwargs.get('project_pk')
        return reverse('tasks:project_detail', kwargs={'project_pk': project_pk})