from django import forms
from .models import Recipe, Step

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title']

# 工程用のフォームセット（複数追加用）
StepFormSet = forms.inlineformset_factory(
    Recipe, Step, fields=('order', 'description'), extra=3, can_delete=True
)