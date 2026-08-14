from django.contrib import admin
from .models import Project, Task, Membership

# Register your models here.
class TaskInline(admin.TabularInline):
    model = Task
    extra = 3

class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 3

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [MembershipInline, TaskInline]

# 単体でも管理できるように登録
@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('project', 'user', 'guest_name')