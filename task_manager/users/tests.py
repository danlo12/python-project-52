from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.core.management import call_command
from task_manager.users.models import CustomUser

#Если я правильно все понял и реализовал, то в следующей итерации переработаю все остальные тесты

class UserRegistrationTest(TestCase):
    def test_register_user(self):
        response = self.client.post(reverse('user-create'), {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(CustomUser.objects.filter(username='testuser').exists())


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