from django.test import Client, TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class InitTest(TestCase):
    """родительский класс от которого все наследуются"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user = User.objects.create_user(username='testuser',
                                        password='12345')
        cls.user = user

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
