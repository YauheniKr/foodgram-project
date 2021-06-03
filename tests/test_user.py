from django.urls import reverse

from .test_init import InitTest


class UserTests(InitTest):
    def setUp(self):
        super().setUp()
        templates_url_names = {
            'registration/login.html': reverse('login'),
            'registration/signup.html': reverse('signup'),
            'registration/password_change_form.html': reverse(
                'password_change'),
            'registration/password_reset_form.html': reverse('password_reset'),
        }
        test_user1 = {
            'first_name': 'testuser2',
            'username': 'testuser2',
            'email': 'test@test.by',
            'password1': '456123Abcd',
            'password2': '456123Abcd',
        }
        self.templates_url_names = templates_url_names
        self.test_user1 = test_user1

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        for template, reverse_name in self.templates_url_names.items():
            with self.subTest(template=template):
                if reverse_name == reverse('login'):
                    response = self.guest_client.get(reverse_name)
                else:
                    response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_pages_address_available(self):
        """URL-адрес доступен."""
        for url_address in self.templates_url_names.values():
            with self.subTest(url_address):
                if url_address == reverse('login'):
                    response = self.guest_client.get(url_address)
                else:
                    response = self.authorized_client.get(url_address)
                self.assertEqual(response.status_code, 200)

    def test_signup_and_redirect(self):
        """Проверяем редирект после создания аккаунта"""
        test_user = {
            'first_name': 'testuser2',
            'username': 'testuser2',
            'email': 'test@test.by',
            'password1': '456123Abcd',
            'password2': '456123Abcd',
        }
        response = self.guest_client.post(reverse('signup'), data=test_user)
        self.assertRedirects(response, reverse('login'))

    def test_login_and_redirect(self):
        """Проверяем редирект после создания входа в аккаунт"""
        test_user = {
            'username': 'testuser',
            'password': '12345',
        }
        response = self.guest_client.post(reverse('login'), data=test_user)
        self.assertRedirects(response, reverse('index'))

    def test_auth_user_login_page_redirect(self):
        """Проверяем редирект auth пользователя со страницы login"""
        response = self.authorized_client.get(reverse('login'))
        self.assertRedirects(response, reverse('index'))


