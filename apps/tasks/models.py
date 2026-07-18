from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=200, blank=True, verbose_name="工程名")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    class Meta:
        verbose_name = "工程"
        verbose_name_plural = "工程一覧"

class Step(models.Model):
    task = models.ForeignKey(Task, related_name='steps', on_delete=models.CASCADE)

    WORK_TYPES = [
        ('cooking', '料理'),
        ('prep', '下準備'),
        ('cleanup', '片付け'),
        ('other', 'その他'),
    ]
    # 作業タイプ（WORK_TYPESを使用）
    work_type = models.CharField(max_length=10, choices=WORK_TYPES, default='cooking', verbose_name="作業タイプ")
    # 工程の詳しい内容
    description = models.TextField(blank=True, verbose_name="説明")
    start = models.PositiveIntegerField(default=0, verbose_name="開始時間（分）")
    duration = models.PositiveIntegerField(default=0, verbose_name="所要時間（分）")

    # 料理のレシピ
    recipe = models.ForeignKey(
            'recipes.Recipe', 
            on_delete=models.SET_NULL, 
            null=True, 
            blank=True, 
            verbose_name="関連レシピ"
        )

    def __str__(self):
        return self.work_type

    def save(self, *args, **kwargs):
        if not self.work_type:
            # 見つからなければ作業を入れる（作業が入ったらバグってる）
            type_label = dict(self.WORK_TYPES).get(self.work_type, "作業")
            self.work_type = type_label
        
        super().save(*args, **kwargs)
