from django.test import TestCase
from django.urls import reverse
from django.core.management import call_command
from django.contrib.messages import get_messages
from task_manager.users.models import CustomUser
import json
from pathlib import Path

class UserRegistrationTest(TestCase):
    def test_register_user(self):
        fixture_path = (Path(__file__).parent.parent / 'users' /
                        'fixtures' /"registration_data.json")
        with open(fixture_path, encoding='utf-8') as f:
            data = json.load(f)
        response = self.client.post(reverse('user-create'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(CustomUser.objects.filter(username='testuser').exists())

        if response.status_code == 302:
            follow_response = self.client.get(response.url)
            messages = list(get_messages(follow_response.wsgi_request))
            self.assertEqual(len(messages), 1)
            self.assertEqual(str(messages[0]), "Пользователь успешно зарегистрирован")

class UserAuthTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        call_command('loaddata', 'users.json', verbosity=0)

    def setUp(self):
        self.user = CustomUser.objects.get(username='testuser')
        self.username = 'testuser'
        self.password = 'testpassword'

    def test_login_user(self):
        response = self.client.post(reverse('login'), {
            'username': self.username,
            'password': self.password
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        if response.status_code == 302:
            follow_response = self.client.get(response.url)
            messages = list(get_messages(follow_response.wsgi_request))
            self.assertEqual(len(messages), 1)
            self.assertEqual(str(messages[0]), "Вы залогинены")

    def test_logout_user(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class UserUpdateTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        call_command('loaddata', 'users.json', verbosity=0)

    def setUp(self):
        self.user = CustomUser.objects.get(username='testuser')
        self.username = 'testuser'
        self.password = 'testpassword'
        self.client.login(username=self.username, password=self.password)

    def test_update_user(self):
        response = self.client.post(reverse('update', args=[self.user.id]), {
            'first_name': 'NewFirstName',
            'last_name': 'NewLastName',
            'username': self.username,
            'password': self.password,
            'password_check': self.password
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'NewFirstName')
        self.assertEqual(self.user.last_name, 'NewLastName')
        if response.status_code == 302:
            follow_response = self.client.get(response.url)
            messages = list(get_messages(follow_response.wsgi_request))
            self.assertEqual(len(messages), 1)
            self.assertEqual(str(messages[0]), "Пользователь успешно изменен")


class UserDeleteTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        call_command('loaddata', 'users.json', verbosity=0)

    def setUp(self):
        self.user = CustomUser.objects.get(username='testuser')
        self.username = 'testuser'
        self.password = 'testpassword'
        self.client.login(username=self.username, password=self.password)

    def test_delete_user(self):
        response = self.client.post(reverse('delete_user', args=[self.user.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(CustomUser.objects.filter(id=self.user.id).exists())
        if response.status_code == 302:
            follow_response = self.client.get(response.url)
            messages = list(get_messages(follow_response.wsgi_request))
            self.assertEqual(len(messages), 1)
            self.assertEqual(str(messages[0]), "Пользователь успешно удален")