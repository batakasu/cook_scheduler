from django import forms
from .models import Project, Task, Membership, Tool
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
        fields = ['title', 'description', 'membership', 'duration']    

    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project', None)
        super().__init__(*args, **kwargs)

        if project is not None:
            self.fields['membership'].queryset = Membership.objects.filter(project=project)
        else:
            self.fields['membership'].queryset = Membership.objects.none()

class ToolForm(forms.ModelForm):
    class Meta:
        model = Tool
        fields = ['name', 'description']

    
    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project', None)
        super().__init__(*args, **kwargs)

TaskFormSet = inlineformset_factory(
    Project,
    Task,
    form=TaskForm,
    extra=1,
    can_delete=True
)
