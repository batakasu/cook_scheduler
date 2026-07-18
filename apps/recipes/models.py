from django.db import models

# Create your models here.
class Recipe(models.Model):
    # 料理名
    title = models.CharField(max_length=15, blank=True, verbose_name="料理名")
    # 作成日時
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")

# Recipeと一対多の関係
class Step(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='steps', on_delete=models.CASCADE)
    # 何番目の工程か
    order = models.PositiveIntegerField(verbose_name="順番")
    duration = models.PositiveIntegerField(default=0, verbose_name="所要時間（分）")
    description = models.TextField(verbose_name="工程内容")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.order}: {self.description[:20]}" 
