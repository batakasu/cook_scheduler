from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings

# Create your models here.
class Project(models.Model):
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

class Membership(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name = 'project', related_name='members')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    guest_name = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        constraints = [
            # 登録ユーザーの場合の重複を防ぐ
            models.UniqueConstraint(fields=['project', 'user'], name='unique_project_user', condition=models.Q(user__isnull=False)),
        ]

    def __str__(self):
        return self.user.username if self.user else self.guest_name

class Tool(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="プロジェクト")
    name = models.CharField(max_length=30, blank=True, verbose_name="道具")
    description = models.TextField(blank=True, verbose_name="備考")
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "道具"
        verbose_name_plural = "道具一覧"

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete = models.CASCADE, verbose_name = '作業', related_name='tasks')
    membership = models.ForeignKey(Membership, on_delete = models.SET_NULL, null=True, verbose_name="担当者", related_name='member')
    title = models.CharField(max_length=30, blank=True, verbose_name="作業名")
    description = models.TextField(blank=True, verbose_name="備考")
    # 順序の管理
    order = models.PositiveIntegerField(default=0, verbose_name="順番")
    # 手をはなせるか（False = はなせない）
    leave = models.BooleanField(default=False)
    # 関連するタスク
    from_task = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    # 時間の管
    # スタートからどれだけ時間を空けるか
    start_offset = models.IntegerField(default=0, verbose_name="オフセット（分）")
    duration = models.PositiveIntegerField(default=0, verbose_name="所要時間（分）")

    def __str__(self):
        return f"{self.order}: {self.title}"

    def find_first_task(self):
        first_task = self
        s = set()

        while(first_task.from_task is not None):
            if first_task.id in s:
                raise ValidationError('処理済みです')
            
            s.add(first_task.id)
            first_task = first_task.from_task

        return first_task

    def find_next_tasks(self):
        next_tasks = self.project.tasks.filter(from_task=self.id)
        return next_tasks

    def update_next_task_offsets(self, s=None):
        if s is None:
            s = set()
            s.add(self.id)

        for t in self.find_next_tasks():
            if t.id in s:
                raise ValidationError('処理済みです')

            s.add(t.id)
            t.start_offset = self.start_offset + self.duration
            t.save(update_fields=['start_offset'])
            t.update_next_task_offsets(s)

    def find_conflicting_tasks(self):
        s = set()
        
        if self.leave is True or self.membership is None:
            return s

        target_tasks = self.project.tasks.filter(membership=self.membership).filter(leave=False).exclude(id=self.id)
        for t in target_tasks:
            if self.start_offset < (t.start_offset + t.duration) and t.start_offset < (self.start_offset + self.duration):
                s.add(t.id)
        return s
            
    class Meta:
        ordering = ["order"]
        verbose_name = "作業"
        verbose_name_plural = "作業一覧"