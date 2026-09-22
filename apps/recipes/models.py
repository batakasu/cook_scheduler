from django.db import models
from django.core.validators import MinValueValidator
from apps.core.choices import TASK_CATEGORY
from django.conf import settings

# Create your models here.
class Recipe(models.Model):
    # 料理名
    title = models.CharField(max_length=15, blank=True, verbose_name="料理名")
    # 作成日時
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    # 公開するか
    is_public = models.BooleanField(default=False)
    # 作った人
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.title

# Recipeと一対多の関係
class Step(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='steps', on_delete=models.CASCADE)
    # 何番目の工程か
    order = models.PositiveIntegerField(verbose_name="順番")
    # 手をはなせるか（False = はなせない）
    leave = models.BooleanField(default=False)
    category = models.CharField(choices=TASK_CATEGORY, default='other')
    duration = models.PositiveIntegerField(default=0, verbose_name="所要時間（分）")
    title = models.CharField(max_length=30, blank=True, verbose_name="作業名")
    description = models.TextField(blank=True, verbose_name="工程内容")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.order}: {self.description[:20]}" 

# Recipeと一対多の関係
class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='recipe_ingredients', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)], blank=True, null=True, verbose_name="使用量")
    name = models.CharField(max_length=30, verbose_name="材料名")
    unit = models.CharField(max_length=30, blank=True, verbose_name="単位")