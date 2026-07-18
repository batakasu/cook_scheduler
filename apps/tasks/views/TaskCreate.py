from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from apps.tasks.models import Task, Step
from apps.tasks.forms import TaskForm, StepFormSet
from django.db import transaction

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:schedule')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            # POST時：送信されたデータでフォームセットを作成
            context['formset'] = StepFormSet(self.request.POST)
        else:
            # 通常時：空のフォームセットを作成
            context['formset'] = StepFormSet()
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        
        if not formset.is_valid():
            return self.form_invalid(form)

        with transaction.atomic():
            recipe = form.cleaned_data.get('recipe')
        
            if recipe:# ★追加：これがターミナルに出るか確認
                print(f"DEBUG: レシピ「{recipe.title}」を検出しました。")
                print(f"DEBUG: このレシピには {recipe.steps.all().count()} 個のステップがあります。")

                parent_task = Task.objects.create(title=recipe.title)
                
                for step in recipe.steps.all():
                    Step.objects.create(
                        task=parent_task,
                        order=step.order,
                        duration=step.duration,
                        description=step.description,
                        recipe=step.recipe
                    )
                print("DEBUG: 展開完了！これからリダイレクトします。")
                return redirect(self.success_url)
            else:
                # 通常の保存処理
                self.object = form.save()
                formset.instance = self.object
                formset.save()
                return super().form_valid(form)