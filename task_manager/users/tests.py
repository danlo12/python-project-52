from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.users.models import CustomUser
from task_manager.tasks.models import Task
from task_manager.labels.models import Label
from task_manager.statuses.models import Status



class UserRegistrationTest(TestCase):
    def test_register_user(self):
        response = self.client.post(reverse('user-create'),{
            'first_name':'John',
            'last_name':'Smith',
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'TestPassword',
            'password_check':'TestPassword',
        })

        self.assertEqual(response.status_code, 302)

        self.assertTrue(CustomUser.objects.filter(username='newuser').exists())


class UserAuthTest(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = get_user_model().objects.create_user(
            username=self.username,
            password=self.password
        )
    def test_login_user(self):
        response = self.client.post(reverse('login'),{
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
    def setUp(self):
        self.username = 'testuser'
        self.password = 'TestPassword123'
        self.user = get_user_model().objects.create_user(
            username=self.username,
            password=self.password,
            first_name='OldFirstName',
            last_name='OldLastName'
        )
        self.client.login(username=self.username, password=self.password)

    def test_update_user(self):
        response = self.client.post(reverse('update',args=[self.user.id]), {
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
    def setUp(self):
        self.username = 'testuser'
        self.password = 'TestPassword123'
        self.user = get_user_model().objects.create_user(
            username=self.username,
            password=self.password,
            first_name='OldFirstName',
            last_name='OldLastName'
        )
        self.client.login(username=self.username, password=self.password)

    def test_delete_user(self):
        response = self.client.post(reverse('delete_user',args=[self.user.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(get_user_model().objects.filter(id=self.user.id).exists())
