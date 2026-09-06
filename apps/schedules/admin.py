from django.contrib import admin
from .models import Project, Task, Membership, Tool

# Register your models here.
class TaskInline(admin.TabularInline):
    model = Task
    extra = 3

class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 3
    
class ToolInline(admin.TabularInline):
    model = Tool
    extra = 3

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [MembershipInline, TaskInline, ToolInline]