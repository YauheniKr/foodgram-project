from decimal import Decimal

from django.db import transaction
from django.forms import ValidationError
from django.shortcuts import get_object_or_404

from .models import Ingredient, RecipeIngredient


def get_request_tags(request):
    return request.GET.getlist('tag', ('Завтрак', 'Обед', 'Ужин'))


def get_ingredients(request):
    out = []
    ingredients = {}
    post = request
    for key, name in post.items():
        if key.startswith('nameIngredient'):
            num = key.partition('_')[-1]
            ingredients['name'] = name
            quantity = post[f'valueIngredient_{num}']
            if Decimal(quantity.replace(',', '.')) <= 0:
                raise ValidationError('Количество ингредиента должно '
                                      'быть больше 0')
            ingredients['quantity'] = post[f'valueIngredient_{num}']
        elif key.startswith('unitsIngredient'):
            ingredients.update({'unit': name})
            test_ingredients = [o.get('name') for o in out]
            if ingredients.get('name') in test_ingredients:
                raise ValidationError('Нельзя добавить '
                                      '2 одинаковых ингредиента')
            out.append(ingredients)
            ingredients = {}
    if not out:
        raise ValidationError('Нужно добавить ингредиент в рецепт')
    return out


def save_recipe(request, ingredients, form):
    with transaction.atomic():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.cooking_time = recipe.cooking_time * 60
        recipe.save()

        objs = []
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
    ingredients = get_ingredients(request.POST)
    with transaction.atomic():
        RecipeIngredient.objects.filter(recipe=instance).delete()
        return save_recipe(request, ingredients, form)
