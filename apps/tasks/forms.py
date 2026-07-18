from django import forms
from .models import Task, Step
from apps.recipes.models import Recipe

class TaskForm(forms.ModelForm):
    # レシピ選択用のフィールドを追加
    recipe = forms.ModelChoiceField(
        queryset=Recipe.objects.all(), 
        required=False, 
        label="レシピから展開"
    )

    class Meta:
        model = Task
        fields = ['title', 'recipe'] # ここに 'recipe' を追加

# 工程用のフォームセット（複数追加用）
StepFormSet = forms.inlineformset_factory(
    Task, Step, fields=('work_type', 'recipe', 'description', 'duration'), extra=3, can_delete=True
)