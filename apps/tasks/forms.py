from django import forms
from .models import Project, Task
from django.forms import inlineformset_factory

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'scheduled_at']
        widgets = {
            'scheduled_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'order', 'start_offset', 'duration']

TaskFormSet = inlineformset_factory(
    Project,
    Task,
    form=TaskForm,
    extra=3,
    can_delete=True
)