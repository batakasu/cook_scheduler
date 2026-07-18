from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from apps.tasks.models import Task
from apps.tasks.forms import TaskForm
from django.db import transaction

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:schedule')

def form_valid(self, form):
        with transaction.atomic():# form.save() は実行せず、データだけ取得する
            recipe = form.cleaned_data.get('recipe')
        
            # もしレシピが選ばれていたら、StepをTaskとして展開
            if recipe:
                steps = recipe.steps.all()
                for step in steps:
                    Task.objects.create(
                        user=self.request.user,
                        title=step.description, 
                        work_type='cooking',
                        recipe=recipe,
                        duration=0 # もしStepに時間があればここに入れる
                    )
            else:
                # レシピがない場合は、通常通り1つのタスクとして保存
                form.instance.user = self.request.user
                form.save()
            
        return redirect(self.success_url)