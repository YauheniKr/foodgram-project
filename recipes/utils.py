from decimal import Decimal
from datetime import timedelta

from django.conf import settings
from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import get_object_or_404

from .models import Ingredient, RecipeIngredient


def get_request_tags(request):
    return request.GET.getlist('tag', ('Завтрак', 'Обед', 'Ужин'))


def get_ingredients(request):
    out = []
    ingredients = {}
    post = request.POST
    for key, name in post.items():
        if key.startswith('nameIngredient'):
            num = key.partition('_')[-1]
            ingredients['name'] = name
            ingredients['quantity'] = post[f'valueIngredient_{num}']
        elif key.startswith('unitsIngredient'):
            ingredients.update({'unit': name})
            out.append(ingredients)
            ingredients = {}
    return out


def save_recipe(request, form):

    with transaction.atomic():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.cooking_time = recipe.cooking_time * 60
        recipe.save()

        objs = []
        ingredients = get_ingredients(request)
        for parts in ingredients:

            ingredient = get_object_or_404(Ingredient, title=parts.get('name'),
                                           unit__dimension=parts.get('unit'))
            objs.append(
                RecipeIngredient(
                    recipe=recipe,
                    ingredient=ingredient,
                    quantity=Decimal(parts.get('quantity').replace(',', '.'))
                )
            )

        RecipeIngredient.objects.bulk_create(objs)
        form.save_m2m()
        return recipe


def edit_recipe(request, form, instance):
    with transaction.atomic():
        RecipeIngredient.objects.filter(recipe=instance).delete()
        return save_recipe(request, form)
