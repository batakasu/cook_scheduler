from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    pass

class CookingGroup(models.Model):
    name = models.CharField(max_length=30, blank=True, verbose_name="グループ名")
    leader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               related_name="leder_cooking_groups", verbose_name="リーダー"
                              )
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
                                     related_name="cooking_groups",verbose_name="メンバー"
                                    )

    def __str__(self):
        return self.name