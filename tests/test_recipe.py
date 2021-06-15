import datetime

from django.urls import reverse

from .test_init import InitTest
from datetime import timedelta
from recipes.models import Recipe, RecipeIngredient, Ingredient, Unit, Tag
from recipes.utils import get_request_tags


class RecipeTests(InitTest):
    def setUp(self):
        super().setUp()
        templates_url_names = {
            'index.html': reverse('index'),
            'formRecipe.html': reverse('add_recipe'),
            'singlePage.html': reverse('detail_recipe', args=[self.recipe.id]),
        }
        self.templates_url_names = templates_url_names

    def test_urls_uses_correct_template(self):
        """URL-адрес recipe использует соответствующий шаблон."""
        for template, reverse_name in self.templates_url_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_pages_address_available(self):
        """URL-адрес recipe доступен."""
        for url_address in self.templates_url_names.values():
            with self.subTest(url_address):
                response = self.authorized_client.get(url_address)
                self.assertEqual(response.status_code, 200)

    def test_correct_cooking_time_render(self):
        response = self.authorized_client.get(reverse('index'))
        self.assertEqual(response.context.get('object_list')[0].cooking_time,
                         self.cooking_time)
