import json
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'foodgram_project.settings')
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
import django
from recipes.models import Unit, Ingredient

django.setup()

file_path = 'ingredients.json'

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
