from django.contrib import admin
from .models import Recipe, Step

# Register your models here.
class StepInline(admin.TabularInline):
    model = Step
    extra = 3

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [StepInline]