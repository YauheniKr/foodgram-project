from django.urls import reverse

from recipes.models import Tag

from .test_init import InitTest


class RecipeTests(InitTest):
    def setUp(self):
        super().setUp()
        templates_url_names = {
            'index.html': reverse('index'),
            'formRecipe.html': reverse('add_recipe'),
            'singlePage.html': reverse('detail_recipe', args=[self.recipe.id]),
            'formRecipe.html': reverse('update_recipe', args=[self.recipe.id]),
            'myFollow.html': reverse('follow'),
            'authorRecipe.html': reverse('author_page', args=[self.user.id]),
            'favorite.html': reverse('favorate_page', args=[self.user.id]),
            'shopList.html': reverse('purchase_page'),
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

    def test_correct_tag_render(self):
        response = self.authorized_client.get(reverse('index'))
        self.assertIn(response.context.get('object_list')[0].tags.all()[0],
                      Tag.objects.all())
