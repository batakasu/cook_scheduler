from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from apps.tasks.models import Task
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
            context['formset'] = StepFormSet(self.request.POST)
        else:
            context['formset'] = StepFormSet()
        return context
    
    def form_valid(self, form):
        with transaction.atomic():
            recipe = form.cleaned_data.get('recipe')
            context = self.get_context_data()
            formset = context['formset']
        if not formset.is_valid():
            return self.form_invalid(form)

        with transaction.atomic():
            recipe = form.cleaned_data.get('recipe')
        
            if recipe:
                current_start_time = 0
                for step in recipe.steps.all():
                    Task.objects.create(
                        title=step.description, 
                        work_type='cooking',
                    )
                    current_start_time += step.duration
            else:
                self.object = form.save()
                formset.instance = self.object
                formset.save()
        
        return redirect(self.success_url)