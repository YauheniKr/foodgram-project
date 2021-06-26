from django import forms

from .models import Recipe


class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        exclude = ('author', 'created', 'slug', 'ingredients', )
        widgets = {'tags': forms.CheckboxSelectMultiple()}
