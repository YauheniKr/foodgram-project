from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag, Unit

User = get_user_model()


class InitTest(TestCase):
    """родительский класс от которого все наследуются"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cooking_time = timedelta(seconds=1200)
        user = User.objects.create_user(username='testuser',
                                        password='12345')
        unit = Unit.objects.create(dimension='г')
        tags = Tag.objects.create(title='Завтрак', display_name='Breakfast',
                                  color='orange')
        ingr1 = Ingredient.objects.create(title='ингр1',
                                          unit=unit)
        recipe = Recipe.objects.create(
            author=user, title='Recipe_title',
            text='Recipe text', cooking_time=cooking_time,
        )
        recipe.tags.add(tags)
        recipe.save()
        recipe_ingredient = RecipeIngredient.objects.create(recipe=recipe,
                                                            ingredient=ingr1,
                                                            quantity=100)

        cls.user = user
        cls.tags = tags
        cls.ingr = ingr1
        cls.recipe = recipe
        cls.cooking_time = cooking_time

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
