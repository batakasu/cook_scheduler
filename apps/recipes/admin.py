from django.contrib import admin
from .models import Recipe, Step, RecipeIngredient

# Register your models here.
class StepInline(admin.TabularInline):
    model = Step
    extra = 3

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [StepInline, RecipeIngredientInline]
