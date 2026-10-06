from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    display_name = models.CharField(max_length=30, blank=True, verbose_name="表示名")

    @property
    def display_name_or_username(self):
        return self.display_name or self.username

    def __str__(self):
        if self.display_name:
            return f"{self.display_name} (@{self.username})"
        return f"@{self.username}"

class CookingGroup(models.Model):
    name = models.CharField(max_length=30, blank=True, verbose_name="グループ名")
    leader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               related_name="leader_cooking_groups", verbose_name="リーダー"
                              )
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
                                     related_name="cooking_groups",verbose_name="メンバー"
                                    )

    def __str__(self):
        return self.name