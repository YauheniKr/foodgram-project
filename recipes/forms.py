from .models import Recipe, RecipeIngredient, Ingredient, Unit
from django import forms


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        exclude = ('author', 'created', 'slug', )