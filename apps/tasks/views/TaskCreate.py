from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.tasks.models import Task
from apps.tasks.forms import TaskForm

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:schedule')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)