from django import forms
from .models import Recipe, Step

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title']

# 工程用のフォームセット（複数追加用）
StepFormSet = forms.inlineformset_factory(
    Recipe, 
    Step, 
    fields=('order', 'title', 'leave', 'category', 'duration', 'description'), 
    extra=0, 
    can_delete=True,
    widgets={
        'order': forms.HiddenInput(),
    }
)