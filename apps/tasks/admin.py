from django.contrib import admin
from .models import Project, Task

# Register your models here.
class TaskInline(admin.TabularInline):
    model = Task
    extra = 3

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [TaskInline]