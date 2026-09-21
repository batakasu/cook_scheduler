from django.db.models import Q
from .models import Recipe

def accessible_recipes(user):
    return Recipe.objects.filter(
        Q(user=user) | Q(is_public=True)
    )