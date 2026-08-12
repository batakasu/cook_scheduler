from django.views import generic
from django.urls import reverse
from apps.tasks.models import Task
from apps.tasks.forms import TaskForm

class TaskDetail(generic.DetailView, generic.edit.ModelFormMixin):
    pk_url_kwarg = 'task_pk'
    model =Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'
    form_class = TaskForm

    def get_initial(self):
        initial = super().get_initial()
        task = self.get_object()
        initial.update({
            'title': task.title,
            'start_offset': task.start_offset,
            'duration': task.duration,
        })
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_form'] = context['form']
        return context
    
    def post(self, request, *args, **kwargs):
        # 405エラーを防ぐために、postが呼ばれたときに self.object を確実にセットする
        self.object = self.get_object()
        
        form = TaskForm(**self.get_form_kwargs())
        if form.is_valid():
            task = form.save(commit=False)
            task.project_id = self.kwargs.get('project_pk')
            task.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
    def get_success_url(self):
        project_pk = self.kwargs.get('project_pk')
        return reverse('tasks:project_detail', kwargs={'project_pk': project_pk})