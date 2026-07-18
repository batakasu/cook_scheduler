from django import forms
from .models import Task, Step

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title']

# 工程用のフォームセット（複数追加用）
StepFormSet = forms.inlineformset_factory(
    Task, Step, fields=('work_type', 'recipe', 'description', 'duration'), extra=3, can_delete=True
)