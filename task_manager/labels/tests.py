from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.models import CustomUser, Label, Status, Task


class LabelsListViewTest(TestCase):

    def setUp(self):
        # Создаем пользователя
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.label = Label.objects.create(name='Active')
        self.url = reverse('labels')

    def test_labels_list_authenticated(self):
        # Логинимся и проверяем, что страница статусов доступна
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Active')

class LabelsCreateViewTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.url = reverse('label_create')

    def test_create_label_authenticated(self):
        # Логинимся и создаем новый статус
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.url, {'name': 'New Label'})
        self.assertEqual(response.status_code, 302)  # Статус 302, т.к. будет редирект на страницу списка
        self.assertRedirects(response, reverse('labels'))
        self.assertTrue(Label.objects.filter(name='New Label').exists())

class LabelUpdateViewTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.label = Label.objects.create(name='Old Label')
        self.url = reverse('label_update', args=[self.label.id])

    def test_update_label_authenticated(self):
        # Логинимся и обновляем статус
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.url, {'name': 'Updated Label'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('labels'))
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'Updated Label')

class LabelDeleteViewTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.label = Label.objects.create(name='Label to be deleted')
        self.url = reverse('label_delete', args=[self.label.id])

    def test_delete_label_authenticated(self):
        # Логинимся и удаляем статус
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('labels'))
        self.assertFalse(Status.objects.filter(name='Label to be deleted').exists())

