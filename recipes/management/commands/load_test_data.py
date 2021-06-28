import json
import os

from django.core.management.base import BaseCommand

from recipes.models import Unit, Ingredient


class Command(BaseCommand):
    help = 'Загружает данные об ингредиентах и их размерностях'

    def handle(self, *args, **options):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = (os.path.dirname(os.path.dirname(current_dir)) +
                     '\ingredients.json')

        with open(file_path) as file:
            f = json.load(file)
            units = {row.get('dimension') for row in f if row.get('dimension')}
            for unit in units:
                Unit.objects.get_or_create(dimension=unit)
            for row in f:
                if row.get('dimension'):
                    unit = Unit.objects.get(dimension=row.get('dimension'))
                    Ingredient.objects.get_or_create(
                        title=row.get('title'), unit=unit
                    )
