from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.statuses.models import Status


class StatusesListViewTest(TestCase):

    def setUp(self):
        # Создаем пользователя
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.status = Status.objects.create(name='Active')
        self.url = reverse('statuses')  # предполагается, что url для списка статусов называется 'statuses'

    def test_statuses_list_authenticated(self):
        # Логинимся и проверяем, что страница статусов доступна
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Active')


class StatusesCreateViewTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.url = reverse('status_create')  # предполагается, что url для создания статуса называется 'status_create'

    def test_create_status_authenticated(self):
        # Логинимся и создаем новый статус
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.url, {'name': 'New Status'})
        self.assertEqual(response.status_code, 302)  # Статус 302, т.к. будет редирект на страницу списка
        self.assertRedirects(response, reverse('statuses'))  # После создания редирект на страницу статусов
        self.assertTrue(Status.objects.filter(name='New Status').exists())


class StatusesUpdateViewTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.status = Status.objects.create(name='Old Status')
        self.url = reverse('status_update', args=[self.status.id])

    def test_update_status_authenticated(self):
        # Логинимся и обновляем статус
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.url, {'name': 'Updated Status'})
        self.assertEqual(response.status_code, 302)  # Статус 302, т.к. будет редирект на страницу списка
        self.assertRedirects(response, reverse('statuses'))
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Updated Status')


class StatusesDeleteViewTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.status = Status.objects.create(name='Status to be deleted')
        self.url = reverse('status_delete', args=[self.status.id])

    def test_delete_status_authenticated(self):
        # Логинимся и удаляем статус
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses'))
        self.assertFalse(Status.objects.filter(name='Status to be deleted').exists())
