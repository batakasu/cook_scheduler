from django.db import models

# Create your models here.
class Recipe(models.Model):
    # 料理名
    title = models.CharField(max_length=15, blank=True, verbose_name="料理名")

class Step(models.Model):
    # Recipeと一対多の関係
    recipe = models.ForeignKey(Recipe, related_name='steps', on_delete=models.CASCADE)
    order = models.PositiveIntegerField(verbose_name="順番") # 何番目の工程か
    description = models.TextField(verbose_name="工程内容")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.order}: {self.description[:20]}" 
