from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Task(models.Model):

    WORK_TYPES = [
        ('cooking', '料理'),
        ('prep', '下準備'),
        ('cleanup', '片付け'),
        ('other', 'その他'),
    ]
    # 作業タイプ（WORK_TYPESを使用）
    work_type = models.CharField(max_length=10, choices=WORK_TYPES, default='cooking', verbose_name="作業タイプ")

    # 料理名または工程のタイトル
    title = models.CharField(max_length=200, blank=True, verbose_name="工程名")
    # 工程の説明
    description = models.TextField(blank=True, verbose_name="説明")
    # 所要時間（分単位）
    duration = models.PositiveIntegerField(default=0, verbose_name="所要時間(分)")
    # 作成日時
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.title:
            # 見つからなければ作業を入れる（作業が入ったらバグってる）
            type_label = dict(self.WORK_TYPES).get(self.work_type, "作業")
            self.title = type_label
        
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "工程"
        verbose_name_plural = "工程一覧"