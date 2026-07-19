from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings

# Create your models here.
class Project(models.Model):
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='projects')
    title = models.CharField(max_length=30, blank=True, verbose_name="献立名")
    description = models.TextField(blank=True, verbose_name="備考")
    scheduled_at = models.DateTimeField(null=True, blank=True, verbose_name="調理予定日時")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "献立"
        verbose_name_plural = "献立一覧"

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete = models.CASCADE, verbose_name = '献立', related_name='tasks')
    title = models.CharField(max_length=30, blank=True, verbose_name="作業名")
    description = models.TextField(blank=True, verbose_name="備考")
    # 順序の管理
    order = models.PositiveIntegerField(default=0, verbose_name="順番")
    # 時間の管
    # プロジェクト開始から「何分後」に開始するか（相対時間）
    start_offset = models.PositiveIntegerField(default=0, verbose_name="開始オフセット（分）")
    duration = models.PositiveIntegerField(default=0, verbose_name="所要時間（分）")

    def __str__(self):
            return f"{self.order}: {self.title}"
    
    class Meta:
        ordering = ["order"]
        verbose_name = "作業"
        verbose_name_plural = "作業一覧"