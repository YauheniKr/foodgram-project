from .models import Recipe, RecipeIngredient, Ingredient, Unit, Tag
from django import forms


class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        exclude = ('author', 'created', 'slug', 'ingredients', )
        widgets = {'tags': forms.CheckboxSelectMultiple()}
