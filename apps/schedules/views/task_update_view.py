from django.views import generic
from django.urls import reverse
from apps.schedules.models import Task
from apps.schedules.forms import TaskForm
from ..permissions import accessible_tasks
from django.contrib.auth.mixins import LoginRequiredMixin

class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    pk_url_kwarg = 'task_pk'
    model = Task
    template_name = 'schedules/task_detail.html'
    context_object_name = 'task'
    form_class = TaskForm

    def get_queryset(self):
        tasks = accessible_tasks(self.request.user).filter(project_id=self.kwargs['project_pk'])
        return tasks

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_form'] = context['form']
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project'] = self.object.project
        return kwargs
    
    def get_success_url(self):
        project_pk = self.kwargs.get('project_pk')
        return reverse('schedules:project_detail', kwargs={'project_pk': project_pk})